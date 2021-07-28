from core.elements import MessageSession

from .tables import WikiTargetSetInfo, WikiInfo
import json
from .orm import session


class WikiTargetInfo:
    def __init__(self, msg: MessageSession):
        self.msg = msg
        self.query = session.query(WikiTargetSetInfo).filter_by(targetId=msg.target.targetId).first()
        if self.query is None:
            session.add_all([WikiTargetSetInfo(targetId=self.msg.target.targetId, iws='{}', headers='{}')])
            session.commit()

    def add_start_wiki(self, url):
        self.query.link = url
        session.commit()
        return True

    def get_start_wiki(self):
        get = self.query.link
        if get is not None:
            return get
        return False

    def config_interwikis(self, iw: str, iwlink: str = None, let_it=True):
        interwikis = json.loads(self.query.iws)
        if let_it:
            interwikis[iw] = iwlink
        else:
            if iw in interwikis:
                del interwikis[iw]
        self.query.iws = json.dumps(interwikis)
        session.commit()
        return True

    def get_interwikis(self):
        q = self.query.iws
        if q is not None:
            iws = json.loads(q)
            return iws
        else:
            return False

    def config_headers(self, headers, let_it: [bool, None] = True):
        headers_ = json.loads(self.query.headers)
        if let_it:
            for x in headers:
                headers_[x] = headers[x]
        elif let_it is None:
            headers_ = {}
        else:
            for x in headers:
                if x in headers_:
                    del headers_[x]
        self.query.headers = json.dumps(headers_)
        session.commit()
        return True

    def get_headers(self):
        q = self.query.headers
        if q is not None:
            headers = json.loads(q)
        else:
            headers = {'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
        return headers


class WikiSiteInfo:
    def __init__(self, api_link):
        self.api_link = api_link
        self.query = session.query(WikiInfo).filter_by(apiLink=api_link).first()

    def get(self):
        if self.query is not None:
            return self.query.siteInfo, self.query.timestamp
        return False

    def update(self, info: dict):
        if self.query is None:
            session.add_all([WikiInfo(apiLink=self.api_link, siteInfo=json.dumps(info))])
        else:
            self.query.siteInfo = json.dumps(info)
        session.commit()
        return True
