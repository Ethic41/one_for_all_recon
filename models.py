#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2022-01-06 22:26:24
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from typing import Optional, List
from pydantic import BaseModel, validator, Field


class Subdomain(BaseModel):
    url: str = Field(..., description="Subdomain URL")

