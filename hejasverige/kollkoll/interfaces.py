# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText

from hejasverige.kollkoll import _


class IKollkoll(form.Schema):
    """ A content object to 'hold' the kollkoll integration view
    """
    text = RichText(title=_(u'Beskrivning'),
                    description=_(u'En beskrivning av Kollkoll'),
                    required=False)


class IKollkollSettings(Interface):

    """Global Kollkoll settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    kollkoll_url = schema.TextLine(title=_(u'API Url'),
                                   description=_(u'help_kollkoll_url',
                                                 default=u'Your Kollkoll url for reading Kollkoll API.'
                                                 ),
                                   required=False, default=u'')

    kollkoll_user = schema.TextLine(title=_(u'User name'),
                                    description=_(u'help_kollkoll_user',
                                                  default=u'Your Kollkoll username for reading Kollkoll API.'
                                                  ),
                                    required=False, default=u'')

    kollkoll_password = schema.TextLine(title=_(u'Password'),
                                        description=_(u'help_kollkoll_password',
                                                      default=u'Your Kollkoll password for reading Kollkoll API.'
                                                      ),
                                        required=False, default=u'')

    kollkoll_timeout = schema.TextLine(title=_(u'Timeout'),
                                       description=_(u'help_kollkoll_timeout',
                                                     default=u'The timeout before stop try reading Kollkoll API.'
                                                     ),
                                       required=False, default=u'5.000')
