# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

from Products.PythonScripts.standard import url_quote
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from hejasverige.kollkoll.interfaces import IKollkollSettings

#URLS
from hejasverige.kollkoll.config import LISTCARDS, LOGIN, ADDCARD, LISTCARDS, UPDATETRANS, LISTTRANS, ADDUSER, ADDCOMPANY, LISTUSERS, REMOVECARD

from lxml import etree
from StringIO import StringIO

import hashlib
import os,binascii

import logging
logger = logging.getLogger(__name__)


class Kollkoll():    
    def __init__(self):
        ''' settings is a RecordsProxy object retreived from kollkoll registry settings
        '''
        #import pdb; pdb.set_trace()
        settings = self.getSettings()
        self.auth = HTTPBasicAuth(settings.kollkoll_user, settings.kollkoll_password)
        self.uid = settings.kollkoll_user
        self.pw = settings.kollkoll_password
        self.url = settings.kollkoll_url
        try:
            self.timeout = float(settings.kollkoll_timeout)
        except:
            logger.exception('Timeout could not be converted to float. Using 10.000 as default.')
            self.timeout = 10.000
        logger.info('Url: ' + self.url)
        logger.info('Timeout: ' + str(self.timeout))

    def getSettings(self):
        ''' Helper function to get the settings provided by kollkoll registry
        '''
        try:
            registry = getUtility(IRegistry)
        except:
            logger.exception('Failed to get utility IRegistry')
            return

        try:
            settings = registry.forInterface(IKollkollSettings)
        except KeyError, ex:
            logger.exception('Got exception: %s' % str(ex))
            return
        return settings

    def login(self):
        logger.info("Kollkoll login")
        #import pdb; pdb.set_trace()
        url = self.url + '/' + LOGIN + '?uid=' + self.uid + '&pw=' + self.pw
        logger.info('login url: %s' % url)
        headers = {'Accept': 'text/xml'}

        logger.info('Headers: ' + str(headers))

        try:
            r = requests.get(url,
                             headers=headers,
                             timeout=self.timeout
                             )
        except Exception, ex:
            logger.exception('Got exception: %s' % str(ex))
            return {}

        # Unable to login with configured credentials
        if 'No user found with id:' in r.text:
            logger.error('Unable to login to Kollkoll with the provided credentials. User: %s' % self.uid)
            return {}

        return_data = {}
        try:
            xmldata = etree.parse(StringIO(r.text))
            sessionid = xmldata.xpath('/xml/sessionid')[0].text
            id = xmldata.xpath('/xml/user')[0].attrib['id']
            uid = xmldata.xpath('/xml/user')[0].attrib['uid']
            return_data = dict(sessionid=sessionid, id=id, uid=uid)
            logger.info('Kollkoll status: ' + str(r.status_code))
            logger.info('Kollkoll returns: ' + r.text)
        except Exception, ex:
            logger.exception('Got exception: %s' % str(ex))
            return {}

        return return_data

    def listCards(self, selecteduid, list_all=False):
        logger.info("Kollkoll listCards")

        login = self.login()

        if list_all:
            url = self.url + '/' + LISTCARDS
        else:
            if login:
                url = self.url + '/' + LISTCARDS + '?uid=' + login.get('uid') + '&selecteduid=' + selecteduid + '&sessionid=' + login.get('sessionid')
            else:
                logger.error('Login method to Kollkoll failed')
                return []

        logger.info('listCards url: %s' % url)
        headers = {'Accept': 'text/xml'}

        logger.info('Headers: ' + str(headers))
        #import pdb; pdb.set_trace()
        try:
            result = requests.get(url,
                             headers=headers,
                             timeout=self.timeout
                             )
        except Exception, ex:
            logger.exception('Got exception: %s' % str(ex))
            return

        return_data = []
        try:
            xmldata = etree.parse(StringIO(result.text))
            banks = xmldata.xpath('//bank')
            for bank in banks:
                return_data.append(dict(id=bank.attrib['id'], ctid=bank.attrib.get('ctid', None), name=bank.attrib['name']))

            logger.info('Kollkoll status: ' + str(result.status_code))
            logger.info('Kollkoll returns: ' + result.text)
        except Exception, ex:
            logger.exception('Got exception: %s' % str(ex))
            return []

        return return_data

    def listUsers(self):
        logger.info("Kollkoll listUsers")

        return_data = []
        login = self.login()
        if login:
            url = self.url + '/' + LISTUSERS + '?uid=' + login.get('uid') + '&sessionid=' + login.get('sessionid')
            logger.info('listUsers url: %s' % url)
            headers = {'Accept': 'text/xml'}

            logger.info('Headers: ' + str(headers))
            #import pdb; pdb.set_trace()
            try:
                result = requests.get(url,
                                 headers=headers,
                                 timeout=self.timeout
                                 )
            except Exception, ex:
                logger.exception('Got exception: %s' % str(ex))
                return

            try:
                xmldata = etree.parse(StringIO(result.text))
                users = xmldata.xpath('//user')
                for user in users:
                    return_data.append(dict(id=user.attrib['id'], uid=user.attrib['uid']))

                logger.info('Kollkoll status: ' + str(result.status_code))
                logger.info('Kollkoll returns: ' + result.text)
            except Exception, ex:
                logger.exception('Got exception: %s' % str(ex))
                return []

        return return_data

    def addUser(self, fn, ln, uid, email):
        """ Adds a user to Kollkoll
        """
        logger.info("Kollkoll addUser")
        
        # generate random, long password
        password = hashlib.sha224(binascii.b2a_hex(os.urandom(30))).hexdigest()

        url = self.url + '/' + ADDUSER + '?uid=' + uid + '&pw=' + password + '&fn=' + url_quote(fn) + '&ln=' + url_quote(ln) + '&email=' + url_quote(email)
        logger.info('addUser url: %s' % url)

        headers = {'Accept': 'text/xml'}

        logger.info('Headers: ' + str(headers))
        #import pdb; pdb.set_trace()
        try:
            result = requests.get(url,
                             headers=headers,
                             timeout=self.timeout
                             )
        except Exception, ex:
            logger.exception('Got exception: %s' % str(ex))
            return False

        try:
            logger.info('Kollkoll status: ' + str(result.status_code))
            logger.info('Kollkoll returns: ' + result.text)
        except Exception, ex:
            logger.exception('Got exception: %s' % str(ex))

        return True


    def addCard(self, uid, ctid, cuid, cpw):
        """ Adds a card to a Kollkoll user
        """
        logger.info("Kollkoll addCard")
        login = self.login()

        if login:
            url = self.url + '/' + ADDCARD + '?uid=' + login.get('uid') + '&pw=' + cpw + '&sessionid=' + login.get('sessionid') + '&selecteduid=' + uid + '&ctid=' + ctid + '&cuid=' + cuid
            logger.info('addCard url: %s' % url)

            headers = {'Accept': 'text/xml'}

            logger.info('Headers: ' + str(headers))
            #import pdb; pdb.set_trace()
            try:
                result = requests.get(url,
                                 headers=headers,
                                 timeout=self.timeout
                                 )
            except Exception, ex:
                logger.exception('Got exception: %s' % str(ex))
                return False

            try:
                logger.info('Kollkoll status: ' + str(result.status_code))
                logger.info('Kollkoll returns: ' + result.text)
            except Exception, ex:
                logger.exception('Got exception: %s' % str(ex))

            return True

        logger.exception('Unable to login to Kollkoll')
        return False

    def removeCard(self, uid, bid):
        """ Removes a card from a Kollkoll user
        """
        logger.info("Kollkoll removeCard")
        login = self.login()

        if login:
            url = self.url + '/' + REMOVECARD + '?uid=' + login.get('uid') + '&sessionid=' + login.get('sessionid') + '&selecteduid=' + uid + '&bid=' + bid
            logger.info('removeCard url: %s' % url)

            headers = {'Accept': 'text/xml'}

            logger.info('Headers: ' + str(headers))
            #import pdb; pdb.set_trace()
            try:
                result = requests.get(url,
                                 headers=headers,
                                 timeout=self.timeout
                                 )
            except Exception, ex:
                logger.exception('Got exception: %s' % str(ex))
                return False

            try:
                logger.info('Kollkoll status: ' + str(result.status_code))
                logger.info('Kollkoll returns: ' + result.text)
            except Exception, ex:
                logger.exception('Got exception: %s' % str(ex))

            return True

        logger.exception('Unable to login to Kollkoll')
        return False