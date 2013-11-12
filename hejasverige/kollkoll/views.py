# -*- coding: utf-8 -*-

from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone import api

from zope.interface import Interface
from collective.beaker.interfaces import ISession
from hejasverige.kollkoll.config import SessionKeys

from Products.CMFCore.utils import getToolByName
from hejasverige.content.interfaces import IMyPages
from hejasverige.kollkoll.interfaces import IKollkoll
from hejasverige.kollkoll.kollkoll import Kollkoll
from hejasverige.kollkoll import _

import logging
logger = logging.getLogger(__name__)

grok.templatedir("templates")


def get_pid():
    user = api.user.get_current()
    pid = user.getProperty('personal_id')
    if type(pid).__name__ == 'object':
        pid = None
    return pid

class KollkollView(grok.View):
    grok.context(IKollkoll)
    grok.name('view')
    grok.require('hejasverige.ViewKollkoll')
    #grok.require('zope2.View')
    grok.template('kollkoll')
    grok.implements(IMyPages)


    def update(self):
        ''' Nothing
        '''
        # import pdb; pdb.set_trace()
        logger.debug('Generating view for kollkoll')
        kollkoll = Kollkoll()

        pid = get_pid()
        self.result = kollkoll.listCards(pid)

        session = ISession(self.request, None)
        session[SessionKeys.available_cards] = self.result
        session.save()


class AddBankView(grok.View):
    grok.context(IKollkoll)
    grok.name('add-bank')
    grok.require('hejasverige.ViewKollkoll')
    grok.template('addbank')
    grok.implements(IMyPages)

    def banks(self):
        kollkoll = Kollkoll()
        result = kollkoll.listCards(get_pid(), list_all=True)
        return result

    def update(self):
        ''' Nothing
        '''
        self.pid = get_pid()
        #import pdb; pdb.set_trace()
        self.return_url = self.request.get('return_url', None)

        if 'form.button.Add' in self.request.form:
            # Try Add card to koll koll
            kollkoll = Kollkoll()
            uid = get_pid()
            ctid = self.request.form.get('bank', None)
            cuid = self.request.form.get('personal_id', None)
            cpw = self.request.form.get('personal_code', None)
            self.result = kollkoll.addCard(uid, ctid, cuid, cpw)

            if self.return_url:
                url = self.return_url
            else:
                url = self.context.absolute_url()
            #import pdb; pdb.set_trace()
            utils = getToolByName(self, "plone_utils")
            utils.addPortalMessage(_('Din inlogging registrerades'), 'info')
            return self.request.response.redirect(url)            


class DeleteBankView(grok.View):
    grok.context(IKollkoll)
    grok.name('delete-bank')
    grok.require('hejasverige.ViewKollkoll')
    #grok.template('addbank')
    #grok.implements(IMyPages)

    def render(self):
        ''' Nothing
        '''
        #import pdb; pdb.set_trace()
        session = ISession(self.request, None)
        card_id = self.request.get('id', None)
        return_url = self.request.get('return_url', None)

        if card_id in [x.get('id') for x in session[SessionKeys.available_cards]]:
            kollkoll = Kollkoll()
            result = kollkoll.removeCard(uid=get_pid(), bid=card_id)
        else:
            utils = getToolByName(self, "plone_utils")
            utils.addPortalMessage(_('Kort med angivet id saknas'), 'error')

        if return_url:
            url = return_url
        else:
            url = self.context.absolute_url()

        return self.request.response.redirect(url)