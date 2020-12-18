
import os
import sys
import requests
import shutil
import textwrap 

from prompts import help_str, bkmk_prompt
from colorama import init, Fore, Style
from pathlib import Path
from bs4 import Tag, NavigableString, BeautifulSoup, element


def is_valid_directory(filename):
    p = Path(filename)
    return p.exists() and p.is_dir()


def to_url(command):
    if 'https://' in command:
        return command
    else:
        return f'https://{command}'


def recur_parse(tag, support_tags, level):
    children = list(tag.children)
    indent = '  ' * level
    wrapper = textwrap.TextWrapper(initial_indent = indent, subsequent_indent = indent)
    if element.Tag not in [type(item) for item in children]:
        if tag.name == 'strong':
            print(wrapper.fill(Fore.YELLOW + Style.BRIGHT + tag.get_text(' ', strip=True) + Fore.RESET))
        elif tag.name == ('h1' or 'h2' or 'h3' or 'h4' or 'h5'):
            print(wrapper.fill(Fore.GREEN + Style.BRIGHT + tag.get_text(' ', strip=True) + Fore.RESET))
        elif tag.name == 'a':
            if (tag.get_text(" ", strip=True)):
                print(wrapper.fill(Fore.BLUE + tag.get_text(' ', strip=True) + Fore.RESET))
        else:
            print(wrapper.fill(Fore.WHITE + Style.DIM + tag.get_text(' ', strip=True) + Fore.RESET))

    else:
        for child in children:
            if isinstance(child, Tag):
                if child.name not in support_tags:
                    continue
                else:
                    next_level = level + 1
                    recur_parse(child, support_tags, next_level)
            elif isinstance(child, NavigableString):
                print(wrapper.fill(Fore.WHITE + Style.DIM + child))


def parse_response(response, support_tags):
    soup = BeautifulSoup(response, 'html.parser')
    level = 0
    recur_parse(soup, support_tags, level)
    print(Style.RESET_ALL + Fore.RESET)


def search(url, dir, filename, support_tags):
    if not is_valid_directory(dir):
        Path(dir).mkdir(parents=True, exist_ok=True)

    headers = {'user-agent': 'tbb/0.0.1'}
    try:
        r = requests.get(url, headers=headers)
    except:
        print(Fore.RED + 'ERROR: Could not reach specified site' + Fore.RESET)
        return

    f = open(filename, "w", encoding="utf-8")
    f.write(r.text)
    f.close()

    parse_response(r.text, support_tags)


def main():
    
    init() # Starts colorama
    dir = './' # Where tabs will be stored

    if len(sys.argv) > 1:
        dir = sys.argv[1]
    if os.path.isdir(dir):
        shutil.rmtree(dir)

    support_tags = ['body', 'html', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'nobr',
                    'a', 'span', 'ul', 'ol', 'li', 'link', 'p', 'table', 'td', 
                    'tr', 'strong', 'article', 'section']
    supported_domains = ['.com', '.org', '.gov', '.net']
    history = []
    commands = ['exit', 'back', 'help', 'history', 'bookmarks']
    previous = ''
    previous_url= ''
    
    print(Fore.GREEN + help_str + Fore.RESET)
    while True:
        print(Fore.GREEN + 'Enter a command or URL: ' +  Fore.RESET)
        command = input('>> ')
        
        if command in commands:
            if command == 'exit':
                break

            elif command == 'back':
                try:
                    last = history.pop()
                    previous = last
                except:
                    print('No Previous Sites')
                    continue
                f = open(last, "r", encoding='utf-8')
                parse_response(f.read(), support_tags)
                f.close()
                continue

            elif command == 'help':
                print(help_str)

            elif command == 'history':
                if history:
                    print(Style.BRIGHT + 'Session History:')
                    for index, tab in enumerate(history):
                        print('    ' + Style.DIM + f'{index}. {tab}')
                    print('    ' + Style.DIM + f'{index+1}. {previous} *')
                    print(Style.RESET_ALL + Fore.RESET)
                else:
                    print('    ' + Style.DIM + f'1. {previous} *')
                    print(Style.RESET_ALL + Fore.RESET)
            
            elif command == 'bookmarks':
                while True:
                    print(bkmk_prompt + Fore.GREEN + '\nChoose an option: ' + Fore.RESET)
                    choice = input('>> ')
                    
                    try:
                        choice = int(choice)
                    except:
                        print(Fore.RED + 'ERROR: Please enter an integer' + Fore.RESET)
                        continue

                    if choice < 1 or choice > 4:
                        print(Fore.RED + 'ERROR: Please enter one of the above choices' + Fore.RESET)
                        continue


                    if choice == 1:     
                        '''
                            Bookmark current site
                        '''
                        if previous_url:
                            with open('bookmarks.txt', 'r', encoding='utf-8') as f:
                                lines = f.read().splitlines() 
                            
                            if previous_url in lines:
                                print(Fore.RED + 'You have already bookmarked this site' + Fore.RESET)
                                continue

                            f = open('bookmarks.txt', 'a')
                            print(f'Bookmarked {previous_url}\n')
                            f.write(previous_url + '\n')
                            f.close()
                            break
                        else:
                            print(Fore.RED + 'You are not currently viewing a site' + Fore.RESET)
                            continue
                        
                    elif choice == 2:
                        '''
                            Open bookmark
                        ''' 
                        with open('bookmarks.txt', 'r', encoding='utf-8') as f:
                            lines = f.read().splitlines() 

                        if not lines:
                            print(Fore.RED + 'You have no bookmarks' + Fore.RESET)
                            continue

                        print('\nBookmarks:')
                        
                        for index, line in enumerate(lines):
                            print(f'{index}. {line}')

                        print(Fore.GREEN + '\nPlease choose a bookmark: ' + Fore.RESET)
                        choice = input('>> ')
                        
                        try:
                            choice = int(choice)
                        except:
                            print(Fore.RED + 'ERROR: Please enter an integer from above' + Fore.RESET)
                            continue

                        if choice < 0 or choice > len(lines) - 1:
                            print(Fore.RED + 'ERROR: Please enter one of the above choices' + Fore.RESET)
                            continue
                        
                        url = lines[choice][8:]
                        if 'https:' in url:
                            url = url[8:]
                        if url.endswith('/'):
                            url = url[:-1]
                        url = url.replace('/', r'.')
                        filename = os.path.join(dir, url)

                        if previous:
                            history.append(previous)
                        previous = filename
                        previous_url = url

                        if(Path(filename).exists()):
                            f = open(filename, "r", encoding='utf-8')
                            data = f.read()
                            f.close()
                            parse_response(data, support_tags)
                        else:
                            search(lines[choice], dir, filename, support_tags)
                        break

                    elif choice == 3:
                        '''
                            Remove bookmark
                        '''
                        with open('bookmarks.txt', 'r', encoding='utf-8') as f:
                            lines = f.read().splitlines()
                        
                        print('\nBookmarks:')
                        for index, line in enumerate(lines):
                            print(f'{index}. {line}')

                        print(Fore.GREEN + '\nPlease choose a bookmark: ' + Fore.RESET)
                        choice = input('>> ')
                        
                        try:
                            choice = int(choice)
                        except:
                            print(Fore.RED + 'ERROR: Please enter an integer from above' + Fore.RESET)
                            continue

                        if choice < 0 or choice > len(lines) - 1:
                            print(Fore.RED + 'ERROR: Please enter one of the above choices' + Fore.RESET)
                            continue
                        
                        removed = lines.pop(choice)
                        lines = map(lambda x: x + '\n', lines)
                        with open('bookmarks.txt', 'w', encoding='utf-8') as f:
                            f.writelines(lines)

                        print(f'Removed {removed}\n')                
                        break

                    elif choice == 4:   # Back
                        break


        elif command not in commands and not any(dom in command for dom in supported_domains):
            print('ERROR: Invalid Command')
            continue

        else:
            url = to_url(command)
            if 'https:' in command:
                command = command[8:]
            if command.endswith('/'):
                command = command[:-1]
            command = command.replace('/', r'.')
            filename = os.path.join(dir, command)
            
            if previous:
                history.append(previous)
            previous = filename
            previous_url = url

            if(Path(filename).exists()):
                f = open(filename, "r", encoding='utf-8')
                data = f.read()
                f.close()
                parse_response(data, support_tags)


            else:
                search(url, dir, filename, support_tags)


if __name__ == '__main__':
    main()