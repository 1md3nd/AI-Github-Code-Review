# import_patterns = {
#     'C': r'#include\s+[<"][\w.]+[">]',  # C include statements
#     'C++': r'#include\s+[<"][\w.]+[">]',  # C++ include statements
#     'Java': r'import\s+\w+(\.\w+)*\s*;',  # Java import statements
#     'Python': r'import\s+\w+|from\s+\w+\s+import\s+\w+',  # Python import statements
#     'Ruby': r'require\s+[\'"]\w+[\'"]',  # Ruby require statements
#     'JavaScript': r'import\s+\w+|require\s*\(\s*["\']\w+["\']\s*\)',  # JavaScript import statements
#     'HTML': r'<link\s+rel="import"\s+href=".*">',  # HTML import statements
#     'CSS': r'@import\s+["\'].*["\']',  # CSS import statements
#     'PHP': r'use\s+\w+(\\{1}\w+)*\s*\\{0,1}\s*as\s*\w+;',  # PHP use statements
#     'Swift': r'import\s+\w+',  # Swift import statements
#     'C#': r'using\s+\w+;',  # C# using statements
#     'Perl': r'use\s+\w+;',  # Perl use statements
#     'R': r'library\s*\(\s*\w+\s*\)',  # R library statements
#     'SQL': r'IMPORT\s+\w+',  # SQL import statements
#     'Go': r'import\s+\(\s*(\w+(\s*\".*\")?\s*,?\s*)*\)',  # Go import statements
#     'Lua': r'require\s+[\'"]\w+[\'"]',  # Lua require statements
#     'Rust': r'extern\s+crate\s+\w+',  # Rust extern crate statements
#     'Shell': r'source\s+[\w./]+',  # Shell source statements
#     'Assembly': r'include\s+[\w.]+',  # Assembly include statements
#     'JSON': r'"\w+":\s*".*"',  # JSON key-value pair
#     'XML': r'xmlns\s*=\s*["\']\w+:\/{2}',  # XML namespace declaration
#     'YAML': r'\w+:\s*.*',  # YAML key-value pair
#     'TOML': r'\w+\s*=\s*.*',  # TOML key-value pair
#     'React JSX': r'import\s+\w+(\.\w+)*\s*;|require\s*\(\s*["\']\w+["\']\s*\)',  # React JSX import statements
#     'React TSX': r'import\s+\w+(\.\w+)*\s*;|require\s*\(\s*["\']\w+["\']\s*\)',  # React TSX import statements
#     'CoffeeScript': r'require\s+[\'"]\w+[\'"]',  # CoffeeScript require statements
#     'TypeScript': r'import\s+\w+(\.\w+)*\s*;|require\s*\(\s*["\']\w+["\']\s*\)',  # TypeScript import statements
#     'Sass': r'@import\s+["\'].*["\']',  # Sass import statements
#     'Less': r'@import\s+["\'].*["\']',  # Less import statements
#     'Kotlin': r'import\s+\w+(\.\w+)*',  # Kotlin import statements
#     'Dart': r'import\s+[\'"]\w+[\'"]',  # Dart import statements
#     'Julia': r'using\s+\w+',  # Julia using statements
#     'Objective-C': r'#import\s+<\w+(\.\w+)*\.h>',  # Objective-C import statements
# }


import_patterns = {
    'C': r'#include\s+[<"]([\w.]+)[">]',  # C include statements
    'C++': r'#include\s+[<"]([\w.]+)[">]',  # C++ include statements
    'Java': r'import\s+(\w+(\.\w+)*)\s*;',  # Java import statements
    'Python': r'import\s+(\w+)|from\s+(\w+)\s+import',  # Python import statements
    'Ruby': r'require\s+[\'"]([\w.]+)[\'"]',  # Ruby require statements
    'JavaScript': r'(?:import\s+(\w+)|require\s*\(\s*[\'"](\w+)[\'"]\s*\))',  # JavaScript import statements
    'HTML': r'<link\s+rel="import"\s+href="([\w./]+)">',  # HTML import statements
    'CSS': r'@import\s+[\'"]([\w./]+)[\'"]',  # CSS import statements
    'PHP': r'use\s+(\w+(\\{1}\w+)*)\s*\\{0,1}\s*as\s*\w+;',  # PHP use statements
    'Swift': r'import\s+([\w.]+)',  # Swift import statements
    'C#': r'using\s+([\w.]+);',  # C# using statements
    'Perl': r'use\s+([\w.]+);',  # Perl use statements
    'R': r'library\s*\(\s*([\w.]+)\s*\)',  # R library statements
    'SQL': r'IMPORT\s+([\w.]+)',  # SQL import statements
    'Go': r'import\s+\(\s*((?:\w+(\s*\".*\")?\s*,?\s*)*)\)',  # Go import statements
    'Lua': r'require\s+[\'"]([\w.]+)[\'"]',  # Lua require statements
    'Rust': r'extern\s+crate\s+([\w.]+)',  # Rust extern crate statements
    'Shell': r'source\s+([\w./]+)',  # Shell source statements
    'Assembly': r'include\s+([\w.]+)',  # Assembly include statements
    'JSON': r'"\w+":\s*"\s*([\w.]+)\s*"',  # JSON key-value pair
    'XML': r'xmlns\s*=\s*["\']([\w.]+):\/{2}',  # XML namespace declaration
    'YAML': r'(\w+):\s*.*',  # YAML key-value pair
    'TOML': r'(\w+)\s*=\s*.*',  # TOML key-value pair
    'React JSX': r'(?:import\s+(\w+(\.\w+)*)\s*;|require\s*\(\s*["\'](\w+(\.\w+)*)["\']\s*\))',  # React JSX import statements
    'React TSX': r'(?:import\s+(\w+(\.\w+)*)\s*;|require\s*\(\s*["\'](\w+(\.\w+)*)["\']\s*\))',  # React TSX import statements
    'CoffeeScript': r'require\s+[\'"]([\w.]+)[\'"]',  # CoffeeScript require statements
    'TypeScript': r'(?:import\s+(\w+(\.\w+)*)\s*;|require\s*\(\s*["\'](\w+(\.\w+)*)["\']\s*\))',  # TypeScript import statements
    'Sass': r'@import\s+[\'"]([\w./]+)[\'"]',  # Sass import statements
    'Less': r'@import\s+[\'"]([\w./]+)[\'"]',  # Less import statements
    'Kotlin': r'import\s+([\w.]+)',  # Kotlin import statements
    'Dart': r'import\s+[\'"]([\w.]+)[\'"]',  # Dart import statements
    'Julia': r'using\s+([\w.]+)',  # Julia using statements
    'Objective-C': r'#import\s+[<"]([\w.]+)\.h[">]',  # Objective-C import statements
}




comment_patterns = {
        'C': r'//.*?$|/\*.*?\*/',  # C-style comments: // and /*
        'C++': r'//.*?$|/\*.*?\*/',  # C++ style comments: // and /*
        'Java': r'//.*?$|/\*.*?\*/',  # Java-style comments: // and /*
        'Python': r'#.*?$',  # Python-style comments: #
        'Ruby': r'#.*?$',  # Ruby-style comments: #
        'JavaScript': r'//.*?$|/\*.*?\*/',  # JavaScript-style comments: // and /*
        'HTML': r'<!--.*?-->|/\*.*?\*/',  # HTML-style comments: <!-- --> and /*
        'CSS': r'/\*.*?\*/',  # CSS-style comments: /* */
        'PHP': r'#.*?$',  # PHP-style comments: #
        'Swift': r'//.*?$',  # Swift-style comments: //
        'C#': r'//.*?$',  # C#-style comments: //
        'Perl': r'#.*?$',  # Perl-style comments: #
        'R': r'#.*?$',  # R-style comments: #
        'SQL': r'--.*?$',  # SQL-style comments: --
        'Go': r'//.*?$',  # Go-style comments: //
        'Lua': r'--.*?$',  # Lua-style comments: --
        'Rust': r'//.*?$',  # Rust-style comments: //
        'Shell': r'#.*?$',  # Shell-style comments: #
        'Assembly': r';.*?$',  # Assembly-style comments: ;
        'JSON': r'//.*?$',  # JSON-style comments: //
        'XML': r'<!--.*?-->|/\*.*?\*/',  # XML-style comments: <!-- --> and /*
        'YAML': r'#.*?$',  # YAML-style comments: #
        'TOML': r'#.*?$',  # TOML-style comments: #
        'React JSX': r'//.*?$|/\*.*?\*/',  # React JSX-style comments: // and /*
        'React TSX': r'//.*?$|/\*.*?\*/',  # React TSX-style comments: // and /*
        'CoffeeScript': r'#.*?$',  # CoffeeScript-style comments: #
        'TypeScript': r'//.*?$',  # TypeScript-style comments: //
        'Sass': r'//.*?$',  # Sass-style comments: //
        'Less': r'//.*?$',  # Less-style comments: //
        'Kotlin': r'//.*?$',  # Kotlin-style comments: //
        'Dart': r'//.*?$',  # Dart-style comments: //
        'Julia': r'#.*?$',  # Julia-style comments: #
        'Objective-C': r'//.*?$',  # Objective-C-style comments: //
        # 'iOS App': r'//.*?$',  # iOS App-style comments: //
        # 'Android App': r'//.*?$',  # Android App-style comments: //
        # 'Dynamic Link Library': r'//.*?$',  # Dynamic Link Library-style comments: //
        # 'Executable': r'//.*?$',  # Executable-style comments: //
        # 'Java Archive': r'//.*?$',  # Java Archive-style comments: //
        # 'Java Web Archive': r'//.*?$',  # Java Web Archive-style comments: //
        # 'Enterprise Archive': r'//.*?$',  # Enterprise Archive-style comments: //
        # 'Debian Package': r'//.*?$',  # Debian Package-style comments: //
        # 'Red Hat Package Manager': r'//.*?$',  # Red Hat Package Manager-style comments: //
        # 'Tarball': r'//.*?$',  # Tarball-style comments: //
        # 'Zip Archive': r'//.*?$',  # Zip Archive-style comments: //
        # 'Gzip Compressed File': r'//.*?$',  # Gzip Compressed File-style comments: //
        # 'Bzip2 Compressed File': r'//.*?$',  # Bzip2 Compressed File-style comments: //
        # 'xz Compressed File': r'//.*?$',  # xz Compressed File-style comments: //
        # 'RAR Archive': r'//.*?$',  # RAR Archive-style comments: //
        # '7-Zip Archive': r'//.*?$',  # 7-Zip Archive-style comments: //
        # 'Tar Gzipped Archive': r'//.*?$',  # Tar Gzipped Archive-style comments: //
        # 'Lzip Compressed File': r'//.*?$',  # Lzip Compressed File-style comments: //
        # 'LZMA Compressed File': r'//.*?$',  # LZMA Compressed File-style comments: //
        # 'LZ4 Compressed File': r'//.*?$',  # LZ4 Compressed File-style comments: //
        # 'Zstandard Compressed File': r'//.*?$',  # Zstandard Compressed File-style comments: //
        # 'CSV': r'#.*?$',  # CSV-style comments: #
        # 'TSV': r'#.*?$',  # TSV-style comments: #
        # 'Excel': r'#.*?$',  # Excel-style comments: #
        # 'PDF': r'%.*?$',  # PDF-style comments: %
        # 'Word': r'%.*?$',  # Word-style comments: %
        # 'Text': r'#.*?$',  # Text-style comments: #
        # 'Markdown': r'<!--.*?-->|/\*.*?\*/|#.*?$',  # Markdown-style comments: <!-- -->, /* */, and #
        # 'Rich Text Format': r'%.*?$',  # Rich Text Format-style comments: %
        # 'PowerPoint': r'%.*?$',  # PowerPoint-style comments: %
        # 'Keynote': r'%.*?$',  # Keynote-style comments: %
        # 'Numbers': r'%.*?$',  # Numbers-style comments: %
        # 'OpenDocument Text': r'%.*?$',  # OpenDocument Text-style comments: %
        # 'OpenDocument Spreadsheet': r'#.*?$',  # OpenDocument Spreadsheet-style comments: #
        # 'OpenDocument Presentation': r'#.*?$',  # OpenDocument Presentation-style comments: #
        # 'OpenDocument Graphics': r'#.*?$',  # OpenDocument Graphics-style comments: #
        # 'OpenDocument Formula': r'#.*?$',  # OpenDocument Formula-style comments: #
    }
