<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <q-toolbar>
          <q-toolbar-title>Ponete en contacto</q-toolbar-title>
        </q-toolbar>
      </q-card-section>
      <q-card-section>
        <q-input dense  class="q-mb-md" label="Tu correo electronico" type="email" rounded outlined/>
        <q-input dense class="q-mb-md" label="Cuerpo del mensaje" type="textarea" rounded outlined />
        <q-input dense  class="q-mb-md" label="Tu nombre completo" type="text" rounded outlined/>
      </q-card-section>
      <q-separator/>
      <q-card-actions align="around">
        <q-btn color="primary" label="enviar"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  emits: [
    // REQUIRED
    'ok', 'hide'
  ],

  methods: {
    show () { // dont touch
      this.$refs.dialog.show()
    },

    hide () { // dont touch
      this.$refs.dialog.hide()
    },

    onDialogHide () {
      // required to be emitted
      // when QDialog emits "hide" event
      this.$emit('hide')
    }
  }
}
</script>
