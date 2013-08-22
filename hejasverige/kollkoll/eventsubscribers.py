# -*- coding: utf-8 -*-

from five import grok

from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from hejasverige.kollkoll.kollkoll import Kollkoll

import logging

logger = logging.getLogger(__name__)


@grok.subscribe(IUserLoggedInEvent)
def getKollkollAccount(event):
    """Creates an account in Kollkoll
       when users signs in (if not already present).
    """

    logger.info("Will make sure %s has a kollkoll account." % event.principal.getId())
    kollkoll = Kollkoll()
    #import pdb; pdb.set_trace()
    personal_id = event.principal.getProperty('personal_id')
    if type(personal_id).__name__ == 'object':
        personal_id = None

    fullname = event.principal.getProperty('fullname')
    if type(fullname).__name__ == 'object':
        personal_id = None

    email = event.principal.getProperty('email')
    if type(email).__name__ == 'object':
        personal_id = None

    if personal_id:
        try:
            result = kollkoll.listUsers()
            personal_ids = [x.get('uid') for x in result]
            #import pdb; pdb.set_trace()
            if personal_id in personal_ids:
                logger.info('User present in kollkoll. Nothing is added')
            else:
                # user had no account in Kollkoll
                # create account
                logger.info('User not present in kollkoll. User %s added.' % (personal_id))
                result = kollkoll.addUser(fn=fullname, ln='', uid=personal_id, email=email)
        except Exception, ex:
            logger.exception('Unable to access Kollkoll. User account (%s) could not be checked: %s' % (personal_id, str(ex)))
            # problems accessing the bank
            pass

    return
