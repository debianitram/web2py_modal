#!/usr/bin/env python
#-*- encoding:utf-8 -*-

# Colmena Labs
# debianitram (at) gmail.com


from gluon import current
from gluon.dal import Field
from gluon.sqlhtml import SQLFORM
from gluon.html import TAG, OPTION

from .modal_base import ModalBase

class modalFieldReference(ModalBase):
    """autocomplete es None o el nombre del campo representativo del form"""

    def __init__(self, field, autocomplete=None, **kwargs):
        ModalBase.__init__(self, **kwargs)

        self.field = field
        self.autocomplete = autocomplete

        if not self.field.type.startswith('reference'):
            raise SyntaxError("Sólo puede ser usado con campos referenciados")
        if not hasattr(self.field.requires, 'options'):
            raise SyntaxError("No pueden determinarse las opciones")

    def content(self):

        formnamemodal = "form_%s" % self.modal_key
        table = self.field._db[self.field.type[10:]]
        _cmd, params = None, {}

        form = SQLFORM(table, formname=formnamemodal)

        if form.accepts(current.request.vars,
                        current.session,
                        formname=formnamemodal):

            if self.autocomplete in ('option', 'OPTION', OPTION):
                options = TAG[''](*[OPTION(v,
                                _value=k,
                                _selected=str(form.vars.id) == str(k))
                                for (k, v) in self.field.requires.options()])
                
                _cmd += "$('#%(modal_key)s').html('%(options)s');"
                params = {'modal_key': self.modal_key,
                          'options': options.xml().replace("'", "\'")}
            
            elif isinstance(self.autocomplete, Field):
                fieldtarget = str(table[self.autocomplete.name]).replace('.', '_')
                _cmd += "$('#%(modal_key)s').val('%(autocomplete)s');"
                _cmd += "$('#_autocomplete_%(ftarget)s_auto').val(%(id)s);"

                params = {'modal_key': self.modal_key,
                          'autocomplete': form.vars[self.autocomplete.name],
                          'id': form.vars.id,
                          'ftarget': fieldtarget}


            current.response.flash = "Se creó el registro"
            current.response.js = self.js(form, _cmd, **params)

        elif form.errors:
            current.response.flash = "Controle el formulario"

        return form