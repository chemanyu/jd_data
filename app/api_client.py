import requests
from datetime import datetime

class APIClient:
    def __init__(self):
        self.base_url = "http://ad-ocpx.zhltech.net/attribution/data"
    
    def get_attribution_data(self, date):
        """
        获取归因数据
        
        Args:
            date (str): 查询日期，格式：YYYYMMDD
            
        Returns:
            dict: API返回的数据，如果请求失败返回None
        """
        try:
            params = {'date': date}
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == 0:
                return data
            else:
                print(f"API返回错误: {data.get('message', '未知错误')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求API失败: {e}")
            return None
        except ValueError as e:
            print(f"解析JSON失败: {e}")
            return None
    
    @staticmethod
    def format_date(date_str):
        """
        格式化日期字符串
        
        Args:
            date_str (str): 日期字符串，支持多种格式
            
        Returns:
            str: 格式化后的日期字符串 (YYYYMMDD)
        """
        try:
            # 如果已经是8位数字格式，直接返回
            if len(date_str) == 8 and date_str.isdigit():
                return date_str
            
            # 尝试解析常见的日期格式
            formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d']
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    return date_obj.strftime('%Y%m%d')
                except ValueError:
                    continue
            
            # 如果都无法解析，返回原字符串
            return date_str
            
        except Exception as e:
            print(f"日期格式化失败: {e}")
            return date_str
    
    @staticmethod
    def get_error_type_description(error_type):
        """
        获取错误类型的中文描述
        
        Args:
            error_type (str): 错误类型代码
            
        Returns:
            str: 错误类型的中文描述
        """
        error_descriptions = {
            'channer_not_found': '链接异常',
            'cid_callback_error': '归因异常',
            'cid_callback_empty': '归因字段为空',
            'parse_callback_raw_error': '数据解析异常',
            'p1_missing': '平台异常',
            'send_track_flag_false': '回传字段判断不通过',
            'advertiser_rate_false': '扣量过滤'
        }
        return error_descriptions.get(error_type, error_type)
    
    @staticmethod
    def parse_api_response(data):
        """
        解析API响应数据
        
        Args:
            data (dict): API返回的数据
            
        Returns:
            dict: 解析后的数据结构
        """
        if not data or data.get('code') != 0:
            return None
        
        api_data = data.get('data', {})
        
        # 解析总请求数据
        total_requests = api_data.get('total_requests', {})
        
        # 解析错误统计数据
        error_counts = api_data.get('error_counts', {})
        
        # 解析汇总数据
        summary = api_data.get('summary', {})
        
        # 处理错误类型描述
        error_types_with_desc = {}
        for error_type, count in summary.get('error_types', {}).items():
            error_types_with_desc[error_type] = {
                'count': count,
                'description': APIClient.get_error_type_description(error_type)
            }
        
        return {
            'date': api_data.get('date'),
            'total_requests': total_requests,
            'error_counts': error_counts,
            'summary': {
                'total_request_count': summary.get('total_request_count', 0),
                'total_error_count': summary.get('total_error_count', 0),
                'error_types': error_types_with_desc
            }
        }
