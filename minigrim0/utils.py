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
    
    # Convert *italic* to \textit{} (no space after first *)
    value = re.sub(r'\*([^*\s][^*]*)\*', r'\\textit{\1}', value)
    
    # Convert markdown lists to LaTeX
    value = _convert_markdown_lists(value)
    
    return value


def _convert_markdown_lists(text):
    """Convert markdown lists to LaTeX itemize/enumerate"""
    if not text:
        return text
    
    lines = text.split('\n')
    result_lines = []
    in_unordered_list = False
    in_ordered_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for unordered list items (- or *)
        if re.match(r'^[-*]\s+(.+)$', line):
            match = re.match(r'^[-*]\s+(.+)$', line)
            if not in_unordered_list:
                # Close any open ordered list
                if in_ordered_list:
                    result_lines.append('\\end{enumerate}')
                    in_ordered_list = False
                result_lines.append('\\begin{itemize}[leftmargin=0.6cm, itemsep=0pt]')
                in_unordered_list = True
            result_lines.append(f'\\item {match.group(1)}')
            
        # Check for ordered list items (1. 2. etc.)
        elif re.match(r'^\d+\.\s+(.+)$', line):
            match = re.match(r'^\d+\.\s+(.+)$', line)
            if not in_ordered_list:
                # Close any open unordered list
                if in_unordered_list:
                    result_lines.append('\\end{itemize}')
                    in_unordered_list = False
                result_lines.append('\\begin{enumerate}[leftmargin=0.6cm, itemsep=0pt]')
                in_ordered_list = True
            result_lines.append(f'\\item {match.group(1)}')
            
        # Regular line (not a list item)
        else:
            # Close any open lists if we hit a non-empty, non-list line
            if line and (in_unordered_list or in_ordered_list):
                if in_unordered_list:
                    result_lines.append('\\end{itemize}')
                    in_unordered_list = False
                if in_ordered_list:
                    result_lines.append('\\end{enumerate}')
                    in_ordered_list = False
            
            # Add the regular line (preserve empty lines within lists)
            result_lines.append(lines[i])  # Use original line with spacing
        
        i += 1
    
    # Close any remaining open lists
    if in_unordered_list:
        result_lines.append('\\end{itemize}')
    if in_ordered_list:
        result_lines.append('\\end{enumerate}')
    
    return '\n'.join(result_lines)


