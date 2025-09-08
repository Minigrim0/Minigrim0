import re

def latex_markdown(value):
    """Convert basic markdown to LaTeX format"""
    if not value:
        return ""
    
    # First escape special LaTeX characters (except braces used in commands)
    value = value.replace('&', '\\&')
    value = value.replace('%', '\\%') 
    value = value.replace('$', '\\$')
    value = value.replace('#', '\\#')
    value = value.replace('_', '\\_')
    
    # Convert markdown links [text](url) to LaTeX format
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', value)
    
    # Convert **bold** to \textbf{}
    value = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', value)
    
    # Convert *italic* to \textit{}
    value = re.sub(r'\*([^*]+)\*', r'\\textit{\1}', value)
    
    # Now escape remaining braces that are not part of LaTeX commands
    # This is tricky - we need to avoid escaping braces in \url{}, \textbf{}, etc.
    # For now, let's not escape braces at all since they're mainly in URLs
    
    return value


