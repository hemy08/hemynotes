# -*- coding: utf-8 -*-

# 获取指定目录下所有文件列表，并且转成mkdocs中nav的格式

import os
import re
import json
import yaml

script_path = os.getcwd()  # 你的文件路径

script_dir = os.path.basename(script_path)

level = 0

config_file = os.path.join(script_path + "/pages_config.json")

nav_str = ""

JSON_STR_SITE_NAME = "site name"
JSON_STR_SITE_DESC = "site description"
JSON_STR_HOME = "HOME"
JSON_STR_REPO_URL = "repo url"
JSON_STR_COPYRIGHT = "copyright"
JSON_STR_IGNORE_DIRS = "ignore dirs"
JSON_STR_IGNORE_FILE_TYPES = "ignore file types"
JSON_STR_IGNORE_FILES = "ignore files"
JSON_STR_DOCS_DIR = "docs_dir"
JSON_STR_CHAPTERS = "chapter infos"
JSON_STR_CHAPTER_RELA_PATH = "relative path"
JSON_STR_CHAPTER_LINK = "document link"
JSON_STR_FILE_NAME_CVT = "file name convert"
JSON_STR_EXT_LINKS = "external links"
JSON_STR_THEME = "theme"
JSON_STR_PLUGINS = "plugins"
JSON_STR_EXTRA = "extra"
JSON_STR_EXTRA_CSS = "extra_css"
JSON_STR_EXTRA_JS = "extra_javascript"
JSON_STR_MD_EXTENSIONS = "markdown_extensions"

ignore_dir_list = []
ignore_file_types = []
ignore_files = []
chapters = {}
chapter_links = {}


def is_ignore_dir(path):
    base = os.path.basename(path)
    for ignore in ignore_dir_list:
        if ignore == base:
            return 1
    return 0


def is_ignore_files(file_name):
    for ignore in ignore_files:
        if file_name == ignore:
            return 1
    return 0


def is_ignore_file_types(file):
    for ignore in ignore_file_types:
        if file.endswith(ignore):
            return 1
    return 0


def is_file_or_dir_ignore(name):
    return is_ignore_dir(name) or is_ignore_files(name) or is_ignore_file_types(name)


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        return dir_list


def file_name_cvt(file_name):
    result = file_name_cvt_list.get(file_name, "none")
    if result != "none":
        return result
    else:
        return file_name


def del_number_prefix(file_name):
    # 如果目录/文件名带数字前缀，去掉 01_、01-、0.1-、0.1_、01 、01.、
    pattern = re.compile("^[0-9.]*[-_ .]")
    match_obj = re.findall(pattern, file_name)
    if len(match_obj) != 0:
        return file_name[len(match_obj[0]):]
    else:
        return file_name


def write_files_info(root_dir, obs_path, name, level, fp):
    docs_dir = pages_config.get(JSON_STR_DOCS_DIR)
    # 去掉.md后缀
    if name.endswith(".md"):
        file_name = name[:len(name) - 3]
        pos = obs_path.find(root_dir)
        if docs_dir is None:
            path = obs_path[pos + len(root_dir + "/") :]
        else:
            path = obs_path[pos + len(root_dir + "/") + len(docs_dir + "/"):]
        path = path.replace("\\", "/")

        # 文件名自定义转换
        file_name = file_name_cvt(file_name)

        # 如果目录/文件名带数字前缀，去掉
        file_name = del_number_prefix(file_name)

        # README放在根目录
        if file_name == "README":
            fields = level * " " + "- " + path + "\n"
        else:
            fields = level * " " + "- " + file_name + ": " + path + "\n"
        fp.write(fields)


def print_mkdocs_nav(root_dir, file_dir, level, fp):
    dir_name = os.path.basename(file_dir)
    if level != 0:
        dir_name = del_number_prefix(dir_name)
        cvt_name = file_name_cvt_list.get(dir_name)
        if cvt_name:
            dir_name = cvt_name
        fields = level * " " + "- " + dir_name + ":" + "\n"
        fp.write(fields)

    level = level + 2
    dir_list = get_file_list(file_dir)
    if dir_list is None:
        return

    for name in dir_list:
        if is_file_or_dir_ignore(name):
            continue

        # 是一个目录
        obs_path = os.path.abspath(os.path.join(file_dir, name))

        # 根目录的readme文件不加入列表
        if obs_path == os.path.join(root_dir, "README.md"):
            continue

        # 是目录，则递归
        if os.path.isdir(os.path.relpath(obs_path)):
            print_mkdocs_nav(root_dir, obs_path, level, fp)
        else:  # 是一个文件
            write_files_info(root_dir, obs_path, name, level, fp)
    return


file_name_cvt_list = {}
pages_config = {}
external_links = {}


def set_pages_config(data, key):
    if data.get(key) is None:
        pages_config[key] = None
    else:
        pages_config[key] = data[key]


def read_pages_conf():
    with open(config_file, 'r', encoding='utf-8') as f:
        res = f.read(-1)
        data = json.loads(res)
        set_pages_config(data, JSON_STR_SITE_NAME)
        set_pages_config(data, JSON_STR_SITE_DESC)
        set_pages_config(data, JSON_STR_COPYRIGHT)
        set_pages_config(data, JSON_STR_REPO_URL)
        set_pages_config(data, JSON_STR_HOME)
        set_pages_config(data, JSON_STR_THEME)
        set_pages_config(data, JSON_STR_PLUGINS)
        set_pages_config(data, JSON_STR_EXTRA)
        set_pages_config(data, JSON_STR_EXTRA_CSS)
        set_pages_config(data, JSON_STR_EXTRA_JS)
        set_pages_config(data, JSON_STR_MD_EXTENSIONS)
        set_pages_config(data, JSON_STR_DOCS_DIR)
        get_ignore_dir_file_list(data)
        get_chapters(data)
        get_file_name_cvt_list(data)
        get_external_links(data)
        f.close()
    return


def get_ignore_dir_file_list(data):
    dir_list = data[JSON_STR_IGNORE_DIRS]
    ignore_dir_list.extend(dir_list.split(";"))

    file_list = data[JSON_STR_IGNORE_FILES]
    ignore_files.extend(file_list.split(";"))

    file_type_list = data[JSON_STR_IGNORE_FILE_TYPES]
    ignore_file_types.extend(file_type_list.split(";"))


def get_external_links(data):
    links = data[JSON_STR_EXT_LINKS]
    for key in links:
        external_links[key] = links.get(key)


def get_chapters(data):
    links = data[JSON_STR_CHAPTERS]
    for key in links:
        chapters[key] = links.get(key)


def get_file_name_cvt_list(data):
    cvt_list = data[JSON_STR_FILE_NAME_CVT]
    for key in cvt_list:
        file_name_cvt_list[key] = cvt_list.get(key)


def write_mkdocs_file(chapter_name, fp):
    root_dir = script_path + chapters.get(chapter_name)
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        return

    print_mkdocs_nav(script_path, root_dir, 2, fp)


def mkdocs_mermaid_cvt(file, old_strs, new_strs):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line_str in f:
            for idx in range(len(old_strs)):
                if old_strs[idx] in line_str:
                    line_str = line_str.replace(old_strs[idx], new_strs[idx])
            file_data += line_str
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def write_mkdocs_themes(fp):
    fp.write("\n\n")
    yaml.dump({'theme': pages_config[JSON_STR_THEME]}, fp, allow_unicode=True)

    fp.write("\n\n")
    yaml.dump({'plugins': pages_config[JSON_STR_PLUGINS]}, fp, allow_unicode=True)

    fp.write("\n\n")
    yaml.dump({'extra': pages_config[JSON_STR_EXTRA]}, fp, allow_unicode=True)

    fp.write("\n\n")
    yaml.dump({'extra_css': pages_config[JSON_STR_EXTRA_CSS]}, fp, allow_unicode=True)

    fp.write("\n\n")
    yaml.dump({'extra_javascript': pages_config[JSON_STR_EXTRA_JS]}, fp, allow_unicode=True)

    fp.write("\n\n")
    yaml.dump({'markdown_extensions': pages_config[JSON_STR_MD_EXTENSIONS]}, fp, allow_unicode=True)


def yaml_dump_key_values(f, key, conf):
    if not pages_config.get(conf) is None:
        yaml.dump({key: pages_config.get(conf)}, f, allow_unicode=True)
        f.write("\n")


def create_chapter_mkdocs():
    yml_file = os.path.join(script_path + "/mkdocs.yml")
    # 打开文件句柄
    with open(yml_file, 'w', encoding='utf-8') as f:
        yaml_dump_key_values(f, 'site_name', JSON_STR_SITE_NAME)
        yaml_dump_key_values(f, 'site_description', JSON_STR_SITE_DESC)
        yaml_dump_key_values(f, 'repo_url', JSON_STR_REPO_URL)
        yaml_dump_key_values(f, 'copyright', JSON_STR_COPYRIGHT)
        yaml_dump_key_values(f, 'docs_dir', JSON_STR_DOCS_DIR)
        
        write_mkdocs_themes(f)

        f.write("\nnav:\n")

        fields = "  - HOME" + ": " + pages_config.get(JSON_STR_HOME) + "\n"
        f.write(fields)

        for key in chapters:
            write_mkdocs_file(key, f)

        for name in external_links:
            fields = "  - " + name + ": " + external_links.get(name) + "\n"
            f.write(fields)

        f.close()
    return


read_pages_conf()
create_chapter_mkdocs()
mkdocs_mermaid_cvt(os.path.join(script_path + "/mkdocs.yml"),
                   [
                       "format: '!!python/name:pymdownx.superfences.fence_code_format'",
                       "emoji_generator: '!!python/name:pymdownx.emoji.to_png'",
                       "emoji_generator: '!!python/name:materialx.emoji.to_svg'",
                       "emoji_index: '!!python/name:materialx.emoji.twemoji'"
                   ], [
                       "format: !!python/name:pymdownx.superfences.fence_code_format",
                       "emoji_generator: !!python/name:pymdownx.emoji.to_png",
                       "emoji_generator: !!python/name:materialx.emoji.to_svg",
                       "emoji_index: !!python/name:materialx.emoji.twemoji"
                   ]
                   )
