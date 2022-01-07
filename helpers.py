#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2022-01-06 22:39:41
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from typing import Optional, List


def get_line_separated_file_content_from_input(
    input_prompt: str,
    default_file_path: Optional[str] = None,
):
    line_seperated_file = input(f"{{x}} File path => {input_prompt}:\n").strip("\n")

    if not line_seperated_file:
        print("[-] No file path provided, falling back to default file path")

        if not default_file_path:
            raise NoFilePathError("[-] No default file path provided, exiting")        
        
        line_seperated_file = default_file_path
    
    try:
        with open(line_seperated_file) as f:
            file_lines = f.readlines()
        
        if not file_lines:
            raise EmptyFileError(f"{line_seperated_file} is empty")
        
        clean_file_lines: List[str] = []

        for line in file_lines:
            clean_file_lines.append(line.strip().strip("\r\n").strip("\r").strip("\n"))
        
        return clean_file_lines

    except FileNotFoundError as e:
        raise FileNotFoundError(f"{line_seperated_file} not found")


class EmptyFileError(Exception):
    pass

class NoFilePathError(Exception):
    pass