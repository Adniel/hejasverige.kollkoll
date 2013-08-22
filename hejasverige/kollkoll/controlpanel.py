from plone.app.registry.browser import controlpanel
from hejasverige.kollkoll.interfaces import IKollkollSettings
from hejasverige.kollkoll import _


class KollkollSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IKollkollSettings
    label = _(u"Kollkoll settings")
    description = _(u"""Common settings for Kollkoll""")

    def updateFields(self):
        super(KollkollSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(KollkollSettingsEditForm, self).updateWidgets()
        self.widgets['kollkoll_url'].style = u'width: 50%;'


class KollkollSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = KollkollSettingsEditForm
