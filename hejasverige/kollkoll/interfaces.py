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


#from zope.schema.interfaces import IContextSourceBinder
#from zope.schema.vocabulary import SimpleVocabulary
#from Products.CMFCore.utils import getToolByName
#
#@grok.provider(IContextSourceBinder)
#def possibleBanks(context):
#    acl_users = getToolByName(context, 'acl_users')
#    group = acl_users.getGroupById('organizers')
#    terms = []
#
#    if group is not None:
#        for member_id in group.getMemberIds():
#            user = acl_users.getUserById(member_id)
#            if user is not None:
#                member_name = user.getProperty('fullname') or member_id
#                terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

#    return SimpleVocabulary(terms)


from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

card_providers = SimpleVocabulary(
    [SimpleTerm(value=u'0', title=_(u'American Express')),
     SimpleTerm(value=u'1', title=_(u'Handelsbanken')),
     SimpleTerm(value=u'2', title=_(u'SEB'))]
    )


class IKollkollCard(Interface):
    #form.widget(bank=AutocompleteFieldWidget)
    #bankc = schema.Choice(title=_(u'Bank'),
    #                     vocabulary=banks,
    #                     required=False, default=u'')
    from plone.formwidget.autocomplete import AutocompleteFieldWidget
    form.widget(bank=AutocompleteFieldWidget)
    card_provider = schema.Choice(
            title=_(u"Bank"),
            description=_(u"Ange bank"),
            vocabulary=card_providers)

    username = schema.TextLine(title=_(u'Användarnamn'),
                                   description=_(u'help_username',
                                                 default=u'Ditt användarnamn vid förenklad inloggning'
                                                 ),
                                   required=True, default=u'')

    password = schema.TextLine(title=_(u'Lösenord'),
                                   description=_(u'help_password',
                                                 default=u'Ditt lösenord vid förenklad inloggning'
                                                 ),
                                   required=True, default=u'')



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
