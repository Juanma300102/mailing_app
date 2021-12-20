<template>
  <q-page padding>
    <div class="container">
      <div class="row text-h4 q-mb-sm q-pa-sm">
        ¡Hola {{ this.store.getters['currentUser/getCurrentUserName'] }}!
      </div>
      <q-separator/>
      <div class="row q-pa-sm">
        <div class="column col-md-6 col-sm-auto">
          <div class="row text-h2 q-pa-sm">
            Cargá tu archivo CSV
          </div>
          <div class="row q-pa-sm">
            Para empezar, vas a tener que cargar una lista en formato csv con los destinatarios del mailing. Recorda que no debe tener lineas en blanco, y deben tener sus encabezados <b>correo, nombre, apellido y dni</b>. Si tenes cualquier duda, podes consultar la <a href="some docu">guía</a>.
          </div>
        </div>
        <div class="column col-md-6 col-sm-auto">
          <div class="row">
            <q-uploader
              color="accent"
              flat
              class="col"
              label="Aca podes arrastrar y soltar tu archivo"
            >
            </q-uploader>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { useStore } from 'vuex'

export default {
  name: 'Principal',
  setup () {
    const store = useStore()
    return {
      store
    }
  }
}
</script>
