"""
HTML标签清理工具
用于移除聊天提示词中的HTML格式标签
"""
import re
from typing import Optional


class HTMLCleaner:
    """HTML标签清理器"""
    
    # HTML标签正则表达式
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
    
    # 常见的HTML实体
    HTML_ENTITIES = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': "'",
        '&nbsp;': ' ',
        '&copy;': '©',
        '&reg;': '®',
        '&trade;': '™'
    }
    
    @classmethod
    def remove_html_tags(cls, text: str) -> str:
        """
        移除HTML标签
        
        Args:
            text: 包含HTML标签的文本
            
        Returns:
            清理后的纯文本
        """
        if not text:
            return ""
        
        # 先处理一些特殊的HTML标签，保留换行
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</div>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</li>', '\n', text, flags=re.IGNORECASE)
        
        # 移除HTML标签
        cleaned_text = cls.HTML_TAG_PATTERN.sub('', text)
        
        # 解码HTML实体
        cleaned_text = cls.decode_html_entities(cleaned_text)
        
        # 清理多余的空白字符
        cleaned_text = cls.clean_whitespace(cleaned_text)
        
        return cleaned_text.strip()
    
    @classmethod
    def decode_html_entities(cls, text: str) -> str:
        """
        解码HTML实体
        
        Args:
            text: 包含HTML实体的文本
            
        Returns:
            解码后的文本
        """
        for entity, char in cls.HTML_ENTITIES.items():
            text = text.replace(entity, char)
        
        # 处理数字实体 &#123; 格式
        def replace_numeric_entity(match):
            try:
                return chr(int(match.group(1)))
            except (ValueError, OverflowError):
                return match.group(0)
        
        text = re.sub(r'&#(\d+);', replace_numeric_entity, text)
        
        # 处理十六进制实体 &#x1A; 格式
        def replace_hex_entity(match):
            try:
                return chr(int(match.group(1), 16))
            except (ValueError, OverflowError):
                return match.group(0)
        
        text = re.sub(r'&#x([0-9a-fA-F]+);', replace_hex_entity, text)
        
        return text
    
    @classmethod
    def clean_whitespace(cls, text: str) -> str:
        """
        清理多余的空白字符
        
        Args:
            text: 需要清理的文本
            
        Returns:
            清理后的文本
        """
        # 将多个连续空白字符替换为单个空格
        text = re.sub(r'\s+', ' ', text)
        
        # 移除行首行尾的空白
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines]
        
        # 移除空行
        cleaned_lines = [line for line in cleaned_lines if line]
        
        return '\n'.join(cleaned_lines)
    
    @classmethod
    def extract_text_from_html(cls, html_text: str) -> str:
        """
        从HTML文本中提取纯文本内容
        
        Args:
            html_text: HTML格式的文本
            
        Returns:
            提取的纯文本
        """
        if not html_text:
            return ""
        
        # 移除HTML标签
        text = cls.remove_html_tags(html_text)
        
        # 进一步清理
        text = cls.clean_whitespace(text)
        
        return text.strip()
    
    @classmethod
    def is_html_content(cls, text: str) -> bool:
        """
        检查文本是否包含HTML标签
        
        Args:
            text: 要检查的文本
            
        Returns:
            如果包含HTML标签返回True，否则返回False
        """
        if not text:
            return False
        
        return bool(cls.HTML_TAG_PATTERN.search(text))


def clean_prompt_text(prompt_text: str) -> str:
    """
    清理提示词文本，移除HTML格式
    
    Args:
        prompt_text: 原始提示词文本
        
    Returns:
        清理后的提示词文本
    """
    return HTMLCleaner.remove_html_tags(prompt_text)


def validate_prompt_format(prompt_text: str) -> dict:
    """
    验证提示词格式
    
    Args:
        prompt_text: 提示词文本
        
    Returns:
        验证结果字典
    """
    result = {
        'is_valid': True,
        'has_html': False,
        'has_markdown': False,
        'cleaned_text': prompt_text,
        'issues': []
    }
    
    if not prompt_text:
        result['is_valid'] = False
        result['issues'].append('提示词为空')
        return result
    
    # 检查是否包含HTML标签
    if HTMLCleaner.is_html_content(prompt_text):
        result['has_html'] = True
        result['issues'].append('包含HTML标签')
        result['cleaned_text'] = HTMLCleaner.remove_html_tags(prompt_text)
    
    # 检查是否包含Markdown格式
    if re.search(r'[*_`#\[\]()]', prompt_text):
        result['has_markdown'] = True
    
    return result
