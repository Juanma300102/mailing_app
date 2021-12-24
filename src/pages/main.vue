<template>
  <q-page padding>
    <div class="container">
      <div class="row text-h4 q-pa-sm">
        Pagina principal
      </div>
      <div class="row q-pa-sm">
        <div class="column col-md-6 col-sm-auto">
          <div class="row text-h2 text-weight-medium">
            ¡Hola {{ this.userName }}!
          </div>
          <div class="row q-pa-sm">
            Para empezar, vas a tener que cargar una lista en formato csv con los destinatarios del mailing. Recorda que no debe tener lineas en blanco, y deben tener sus encabezados <b>correo, nombre, apellido y dni</b>. Si tenes cualquier duda, podes consultar la<a href="some docu"> guía</a>.
          </div>
        </div>
        <q-card class="column col-12 col-md-6 col-sm-12 bg-primary">
          <div class="row">
            <q-uploader
              color="primary"
              flat
              class="col bg-primary"
              label="Aca podes arrastrar y soltar tu archivo"
            >
              <q-icon name="folder"/>
            </q-uploader>
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useQuasar } from 'quasar'

export default {
  name: 'Principal',
  setup () {
    const store = useStore()
    const q = useQuasar()

    const userName = computed(() => {
      return store.getters['currentUser/getCurrentUserName']
    })

    return {
      store,
      q,
      userName
    }
  }
}
</script>
