import datetime

from beanie import Document
from pydantic import BaseModel
from typing import List, Optional, Any
from enum import Enum, IntEnum


class StatusEnum(IntEnum):
    new = 1
    approve = 2
    reject = 5


class CheckAction(str, Enum):
    delete = 'delete'
    export = 'export'


class CheckTlpEnum(str, Enum):
    red = 'red'
    amber = 'amber'
    green = 'green'
    white = 'white'


class CheckTypeEnum(str, Enum):
    attack_pattern = 'Attack-pattern'
    campaign = 'Campaign'
    identity = 'Identity'
    indicator = 'Indicator'
    intrusion_set = 'Intrusion-set'
    malware = 'Malware'
    observed_data = 'Observed-data'
    threat_actor = 'Threat-actor'
    threat_report = 'Threat-report'
    tool = 'Tool'
    vulnerability = 'Vulnerability'


class TiReport(Document):
    code_report: Optional[str] = None
    published_time: Optional[datetime.datetime] = None
    type: List[str]
    title: str
    tlp: CheckTlpEnum
    tag: List[str]
    description: str
    detail: Optional[str] = None
    create_time: Optional[datetime.datetime] = None
    creator: str
    language: str
    languages_parent_id: Optional[str] = None
    status: Optional[StatusEnum] = None
    mark: bool = False
    active: bool = True
    group_id: List[str]

    class Collection:
        name = "report"

    class Config:
        orm_mode = True,
        schema_extra = {
            "example": {
                "type": ["Malware", "Campaign"],
                "title": "Cảnh báo nguy cơ",
                "tlp": "red",
                "tag": ["security", "technology"],
                "description": "Mô tả nội dung báo cáo",
                "detail": "Chi tiết nội dung báo cáo",
                "creator": "request_state=3b17dda4-96e3-4330-871b-0d9761499f49; access_token_cookie=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6M01ZUXdocllWTkFwckpSS1hqR3ZFcC12c083aG1FZVRFbVJ6aklpTmJFIn0.eyJleHAiOjE2NTg5MDg5NzQsImlhdCI6MTY1ODkwODY3NCwiYXV0aF90aW1lIjoxNjU4OTA3NDAzLCJqdGkiOiIzYWRiYWY0Mi1kZjNlLTQ3ODMtYjdiMC01Y2U3YzBhNjcyN2UiLCJpc3MiOiJodHRwOi8vYXV0aC1vbGQudGkudmlzYy5jb20vYXV0aC9yZWFsbXMvYXV0aG9yaXphdGlvbl93cmFwcGVyIiwiYXVkIjpbImF1dGhvcml6YXRpb25fd3JhcHBlciIsImFjY291bnQiXSwic3ViIjoiNWQ5MzA1YTEtNTQ4MC00NGZiLWFiZTUtN2ZlNzZkMTM0NDFkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXV0aG9yaXphdGlvbl93cmFwcGVyIiwic2Vzc2lvbl9zdGF0ZSI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1hdXRob3JpemF0aW9uX3dyYXBwZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgYXVkaWVuY2UgZW1haWwgcHJvZmlsZSIsInNpZCI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic3VwZXJfdXNlciJ9.kbkaiGS47Mzba1kBjc5PuN5gvaZ7Zg2s-r5zyNfza5KcfCntLm7Urxh08JNxneDAXBHeKnn9NBoyjP0X6crt0WnHL8EyoYTGxBjGBmHCrnPCL_BIgFzt7L6D3nJ3sMBpAWZlJPCvAyMsVSK2uPEyYgFsXaCBrPNw14mIprTHrOnSQuovEr7EADwlhyH9bkE5t0_gqSBJ8obvJpJa6657iGHLonU775JX2EEYUhPeBk60fGnFzgcZVl7Hz4OZfBp0b73-ZvLOliMkSA3xbrHGXxv4M0YclEPNDCdJa6YB8mfMqHxtxRkjlSIuI5J-H1syFugdrrV90bRNhkAPxwUQbA; refresh_token_cookie=Wm1CGt1FN0/1Pmle6IFROFnACf9X4Zzert/gNMgaD76t6RPmmL5k8rbit8aAGx5X22USPlORtyozXkFKjk3ekIB63LhhBelDU/tXLDJ5OhgNHr9U9ReUDJCp06u5bNSgmUTcWEntbVSeIa+2mLR3TeEUOaH8sks36vFK1t6V/1/Da6S+WkLHFJXzSq0OfO4oXyeoTtWv+xmjPmD4OmlrrcS1FbCTwFNFx9fhSGzc0CFuDTLAvM+WWCy7k5Bj6mc0LF078n4t50Qc2ROCyQ1+j5c0JGT+HWgmkC2rzYkLKAh46hc7W3Er/RCUn3qYFRAhD/6REIyga4Oe39g5HRBD4ZtiaZfboIpI1WE/3ejOMKr0xlo4tQqwxMO2EYQH05q7gpTsriH36Q3U2pGsLvbn/RbkG7ViAQGs3YhLLbJx9EJiQjUqBtRXOfBA63MTfuYcqpvyIfZP0IVTYCcYfF7SJdn8jwESWJUSgDuCIs+PJSKU4DixnQoOUdpf4h84bkuJKWUix7+PB+vWpz1Cq5il4cEgm8+bEEjfao4bw6iUWlvVVUCty+D9W//LnSBPjnrVnb3oxz7cUnIzK0895JszR5DkzQZRnDOpTiRLrjqqT4NDWbQ06wcpp+uaGd9yrwgVUOUFDBJkFbU/jkuI9mZYgpdv0jfcBUCT9V3elTg4PIK5fSkBxHAOlywOdcFDA+mOmxzD4NZXYXNyDtbmmtVrf4aRtX4tCfEr9uN15qR1o9QVEckvKROjyXlTTBIYy4l0rf3mLkJUzHDP4RwqWYc",
                "language": "VI",
                "languages_parent_id": "8dsf8ds8g8ds8gs2dv",
                "mark": "True",
                "active": "True",
                "group_id": ["abc", "def"]
            }
        }


class TiReportShortView(BaseModel):
    code_report: Optional[str] = None
    published_time: Optional[datetime.datetime] = None
    type: List[str]
    title: str
    tlp: CheckTlpEnum
    tag: List[str]
    description: str
    detail: Optional[str] = None
    create_time: Optional[datetime.datetime] = None
    creator: str
    language: str
    status: StatusEnum
    mark: bool = True
    active: bool = True
    group_id: List[str]

class UpdateReport(BaseModel):
    object_id: str
    cookie: str
    type: List[str]
    title: str
    tlp: CheckTlpEnum
    tag: List[str]
    description: str
    language: str
    detail: Optional[str] = None
    group_id: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "object_id": "62d69ed314e0ec5ab4950128",
                "cookie": "request_state=3b17dda4-96e3-4330-871b-0d9761499f49; access_token_cookie=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6M01ZUXdocllWTkFwckpSS1hqR3ZFcC12c083aG1FZVRFbVJ6aklpTmJFIn0.eyJleHAiOjE2NTg5MDg5NzQsImlhdCI6MTY1ODkwODY3NCwiYXV0aF90aW1lIjoxNjU4OTA3NDAzLCJqdGkiOiIzYWRiYWY0Mi1kZjNlLTQ3ODMtYjdiMC01Y2U3YzBhNjcyN2UiLCJpc3MiOiJodHRwOi8vYXV0aC1vbGQudGkudmlzYy5jb20vYXV0aC9yZWFsbXMvYXV0aG9yaXphdGlvbl93cmFwcGVyIiwiYXVkIjpbImF1dGhvcml6YXRpb25fd3JhcHBlciIsImFjY291bnQiXSwic3ViIjoiNWQ5MzA1YTEtNTQ4MC00NGZiLWFiZTUtN2ZlNzZkMTM0NDFkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXV0aG9yaXphdGlvbl93cmFwcGVyIiwic2Vzc2lvbl9zdGF0ZSI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1hdXRob3JpemF0aW9uX3dyYXBwZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgYXVkaWVuY2UgZW1haWwgcHJvZmlsZSIsInNpZCI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic3VwZXJfdXNlciJ9.kbkaiGS47Mzba1kBjc5PuN5gvaZ7Zg2s-r5zyNfza5KcfCntLm7Urxh08JNxneDAXBHeKnn9NBoyjP0X6crt0WnHL8EyoYTGxBjGBmHCrnPCL_BIgFzt7L6D3nJ3sMBpAWZlJPCvAyMsVSK2uPEyYgFsXaCBrPNw14mIprTHrOnSQuovEr7EADwlhyH9bkE5t0_gqSBJ8obvJpJa6657iGHLonU775JX2EEYUhPeBk60fGnFzgcZVl7Hz4OZfBp0b73-ZvLOliMkSA3xbrHGXxv4M0YclEPNDCdJa6YB8mfMqHxtxRkjlSIuI5J-H1syFugdrrV90bRNhkAPxwUQbA; refresh_token_cookie=Wm1CGt1FN0/1Pmle6IFROFnACf9X4Zzert/gNMgaD76t6RPmmL5k8rbit8aAGx5X22USPlORtyozXkFKjk3ekIB63LhhBelDU/tXLDJ5OhgNHr9U9ReUDJCp06u5bNSgmUTcWEntbVSeIa+2mLR3TeEUOaH8sks36vFK1t6V/1/Da6S+WkLHFJXzSq0OfO4oXyeoTtWv+xmjPmD4OmlrrcS1FbCTwFNFx9fhSGzc0CFuDTLAvM+WWCy7k5Bj6mc0LF078n4t50Qc2ROCyQ1+j5c0JGT+HWgmkC2rzYkLKAh46hc7W3Er/RCUn3qYFRAhD/6REIyga4Oe39g5HRBD4ZtiaZfboIpI1WE/3ejOMKr0xlo4tQqwxMO2EYQH05q7gpTsriH36Q3U2pGsLvbn/RbkG7ViAQGs3YhLLbJx9EJiQjUqBtRXOfBA63MTfuYcqpvyIfZP0IVTYCcYfF7SJdn8jwESWJUSgDuCIs+PJSKU4DixnQoOUdpf4h84bkuJKWUix7+PB+vWpz1Cq5il4cEgm8+bEEjfao4bw6iUWlvVVUCty+D9W//LnSBPjnrVnb3oxz7cUnIzK0895JszR5DkzQZRnDOpTiRLrjqqT4NDWbQ06wcpp+uaGd9yrwgVUOUFDBJkFbU/jkuI9mZYgpdv0jfcBUCT9V3elTg4PIK5fSkBxHAOlywOdcFDA+mOmxzD4NZXYXNyDtbmmtVrf4aRtX4tCfEr9uN15qR1o9QVEckvKROjyXlTTBIYy4l0rf3mLkJUzHDP4RwqWYc",
                "type": ["Malware", "Security"],
                "title": "Cảnh báo nguy cơ",
                "tlp": "red",
                "tag": ["security", "technology"],
                "description": "Mô tả nội dung báo cáo",
                "detail": "Chi tiết nội dung báo cáo",
                "language": "EN",
                "group_id": []
            }
        }


class DeleteReport(BaseModel):
    cookie = str
    reports_delete: List[str]

    class Config:
        schema_extra = {
            "example": {
                "cookie": "request_state=3b17dda4-96e3-4330-871b-0d9761499f49; access_token_cookie=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6M01ZUXdocllWTkFwckpSS1hqR3ZFcC12c083aG1FZVRFbVJ6aklpTmJFIn0.eyJleHAiOjE2NTg5MDg5NzQsImlhdCI6MTY1ODkwODY3NCwiYXV0aF90aW1lIjoxNjU4OTA3NDAzLCJqdGkiOiIzYWRiYWY0Mi1kZjNlLTQ3ODMtYjdiMC01Y2U3YzBhNjcyN2UiLCJpc3MiOiJodHRwOi8vYXV0aC1vbGQudGkudmlzYy5jb20vYXV0aC9yZWFsbXMvYXV0aG9yaXphdGlvbl93cmFwcGVyIiwiYXVkIjpbImF1dGhvcml6YXRpb25fd3JhcHBlciIsImFjY291bnQiXSwic3ViIjoiNWQ5MzA1YTEtNTQ4MC00NGZiLWFiZTUtN2ZlNzZkMTM0NDFkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXV0aG9yaXphdGlvbl93cmFwcGVyIiwic2Vzc2lvbl9zdGF0ZSI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1hdXRob3JpemF0aW9uX3dyYXBwZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgYXVkaWVuY2UgZW1haWwgcHJvZmlsZSIsInNpZCI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic3VwZXJfdXNlciJ9.kbkaiGS47Mzba1kBjc5PuN5gvaZ7Zg2s-r5zyNfza5KcfCntLm7Urxh08JNxneDAXBHeKnn9NBoyjP0X6crt0WnHL8EyoYTGxBjGBmHCrnPCL_BIgFzt7L6D3nJ3sMBpAWZlJPCvAyMsVSK2uPEyYgFsXaCBrPNw14mIprTHrOnSQuovEr7EADwlhyH9bkE5t0_gqSBJ8obvJpJa6657iGHLonU775JX2EEYUhPeBk60fGnFzgcZVl7Hz4OZfBp0b73-ZvLOliMkSA3xbrHGXxv4M0YclEPNDCdJa6YB8mfMqHxtxRkjlSIuI5J-H1syFugdrrV90bRNhkAPxwUQbA; refresh_token_cookie=Wm1CGt1FN0/1Pmle6IFROFnACf9X4Zzert/gNMgaD76t6RPmmL5k8rbit8aAGx5X22USPlORtyozXkFKjk3ekIB63LhhBelDU/tXLDJ5OhgNHr9U9ReUDJCp06u5bNSgmUTcWEntbVSeIa+2mLR3TeEUOaH8sks36vFK1t6V/1/Da6S+WkLHFJXzSq0OfO4oXyeoTtWv+xmjPmD4OmlrrcS1FbCTwFNFx9fhSGzc0CFuDTLAvM+WWCy7k5Bj6mc0LF078n4t50Qc2ROCyQ1+j5c0JGT+HWgmkC2rzYkLKAh46hc7W3Er/RCUn3qYFRAhD/6REIyga4Oe39g5HRBD4ZtiaZfboIpI1WE/3ejOMKr0xlo4tQqwxMO2EYQH05q7gpTsriH36Q3U2pGsLvbn/RbkG7ViAQGs3YhLLbJx9EJiQjUqBtRXOfBA63MTfuYcqpvyIfZP0IVTYCcYfF7SJdn8jwESWJUSgDuCIs+PJSKU4DixnQoOUdpf4h84bkuJKWUix7+PB+vWpz1Cq5il4cEgm8+bEEjfao4bw6iUWlvVVUCty+D9W//LnSBPjnrVnb3oxz7cUnIzK0895JszR5DkzQZRnDOpTiRLrjqqT4NDWbQ06wcpp+uaGd9yrwgVUOUFDBJkFbU/jkuI9mZYgpdv0jfcBUCT9V3elTg4PIK5fSkBxHAOlywOdcFDA+mOmxzD4NZXYXNyDtbmmtVrf4aRtX4tCfEr9uN15qR1o9QVEckvKROjyXlTTBIYy4l0rf3mLkJUzHDP4RwqWYc",
                "reports_delete": ['78dscgh8ewgc8ew7', '8hbc98hc98hc98']
            }
        }


class MarkReport(BaseModel):
    cookie: str
    report_mark: str

    class Config:
        schema_extra = {
            "example": {
                "cookie": "request_state=3b17dda4-96e3-4330-871b-0d9761499f49; access_token_cookie=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6M01ZUXdocllWTkFwckpSS1hqR3ZFcC12c083aG1FZVRFbVJ6aklpTmJFIn0.eyJleHAiOjE2NTg5MDg5NzQsImlhdCI6MTY1ODkwODY3NCwiYXV0aF90aW1lIjoxNjU4OTA3NDAzLCJqdGkiOiIzYWRiYWY0Mi1kZjNlLTQ3ODMtYjdiMC01Y2U3YzBhNjcyN2UiLCJpc3MiOiJodHRwOi8vYXV0aC1vbGQudGkudmlzYy5jb20vYXV0aC9yZWFsbXMvYXV0aG9yaXphdGlvbl93cmFwcGVyIiwiYXVkIjpbImF1dGhvcml6YXRpb25fd3JhcHBlciIsImFjY291bnQiXSwic3ViIjoiNWQ5MzA1YTEtNTQ4MC00NGZiLWFiZTUtN2ZlNzZkMTM0NDFkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXV0aG9yaXphdGlvbl93cmFwcGVyIiwic2Vzc2lvbl9zdGF0ZSI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1hdXRob3JpemF0aW9uX3dyYXBwZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgYXVkaWVuY2UgZW1haWwgcHJvZmlsZSIsInNpZCI6ImY5MTY0MGNkLWQ3MGUtNGVkMi05YTMzLWZkNTk3MWNiMTk4ZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic3VwZXJfdXNlciJ9.kbkaiGS47Mzba1kBjc5PuN5gvaZ7Zg2s-r5zyNfza5KcfCntLm7Urxh08JNxneDAXBHeKnn9NBoyjP0X6crt0WnHL8EyoYTGxBjGBmHCrnPCL_BIgFzt7L6D3nJ3sMBpAWZlJPCvAyMsVSK2uPEyYgFsXaCBrPNw14mIprTHrOnSQuovEr7EADwlhyH9bkE5t0_gqSBJ8obvJpJa6657iGHLonU775JX2EEYUhPeBk60fGnFzgcZVl7Hz4OZfBp0b73-ZvLOliMkSA3xbrHGXxv4M0YclEPNDCdJa6YB8mfMqHxtxRkjlSIuI5J-H1syFugdrrV90bRNhkAPxwUQbA; refresh_token_cookie=Wm1CGt1FN0/1Pmle6IFROFnACf9X4Zzert/gNMgaD76t6RPmmL5k8rbit8aAGx5X22USPlORtyozXkFKjk3ekIB63LhhBelDU/tXLDJ5OhgNHr9U9ReUDJCp06u5bNSgmUTcWEntbVSeIa+2mLR3TeEUOaH8sks36vFK1t6V/1/Da6S+WkLHFJXzSq0OfO4oXyeoTtWv+xmjPmD4OmlrrcS1FbCTwFNFx9fhSGzc0CFuDTLAvM+WWCy7k5Bj6mc0LF078n4t50Qc2ROCyQ1+j5c0JGT+HWgmkC2rzYkLKAh46hc7W3Er/RCUn3qYFRAhD/6REIyga4Oe39g5HRBD4ZtiaZfboIpI1WE/3ejOMKr0xlo4tQqwxMO2EYQH05q7gpTsriH36Q3U2pGsLvbn/RbkG7ViAQGs3YhLLbJx9EJiQjUqBtRXOfBA63MTfuYcqpvyIfZP0IVTYCcYfF7SJdn8jwESWJUSgDuCIs+PJSKU4DixnQoOUdpf4h84bkuJKWUix7+PB+vWpz1Cq5il4cEgm8+bEEjfao4bw6iUWlvVVUCty+D9W//LnSBPjnrVnb3oxz7cUnIzK0895JszR5DkzQZRnDOpTiRLrjqqT4NDWbQ06wcpp+uaGd9yrwgVUOUFDBJkFbU/jkuI9mZYgpdv0jfcBUCT9V3elTg4PIK5fSkBxHAOlywOdcFDA+mOmxzD4NZXYXNyDtbmmtVrf4aRtX4tCfEr9uN15qR1o9QVEckvKROjyXlTTBIYy4l0rf3mLkJUzHDP4RwqWYc",
                "report_mark": '78dscgh8ewgc8ew7'
            }
        }


class FilterReport(BaseModel):
    keyword: Optional[str] = None
    creator: Optional[str] = None
    tag: Optional[List[str]] = None
    language: Optional[List[str]] = None
    type: Optional[List[str]] = None
    tlp: Optional[List[str]] = None
    status: Optional[List[int]] = None
    time: Optional[dict] = None
    offset: int
    size: int

    class Config:
        schema_extra = {
            "example": {
                "keyword": "nguy cơ",
                "creator": "6a2sfe878sa8fsa8df8as",
                "tag": ["security"],
                "language": ["VI", "EN"],
                "type": ["Malware"],
                "tlp": ["red", "amber"],
                "status": [1],
                "offset": 0,
                "size": 0
            }
        }


class ActionReport(BaseModel):
    action: CheckAction
    ids: Optional[List[str]] = None
    keyword: Optional[str] = None
    creator: Optional[str] = None
    organization: Optional[List[str]] = None
    tag: Optional[List[str]] = None
    language: Optional[List[str]] = None
    type: Optional[List[str]] = None
    tlp: Optional[List[str]] = None
    status: Optional[List[int]] = None
    time: Optional[dict] = None
    offset: int
    size: int

    class Config:
        schema_extra = {
            "example": {
                "action": "delete",
                "ids": ["9as3ncd2ioq3eu3dcn389"],
                "keyword": "nguy cơ",
                "creator": "6a2sfe878sa8fsa8df8as",
                "organization": ["abc"],
                "tag": ["security"],
                "language": ["VI", "EN"],
                "type": ["Malware", "Security"],
                "tlp": ["red", "amber"],
                "status": [1, 2],
                "time": {"gte": 1595131478000, "lte": 1595477078000},
                "offset": 0,
                "size": 0
            }
        }


class Response(BaseModel):
    status_code: int
    detail: Optional[Any]
    message: str
    success: bool

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Sample data",
                "message": "Ok",
                "success": True
            }
        }
