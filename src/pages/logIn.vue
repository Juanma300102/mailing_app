<template>
  <q-page padding>
    <div class="row justify-center">
      <div class="col col-md-4 col-sm-7">
        <q-card class="items-center">
          <q-card-section class="">
            <h4 class="title q-mb-sm">Mailing App</h4>
          </q-card-section>
          <q-separator/>
          <q-card-section>
            <h5 class="title q-mb-md q-mt-sm">Inicio de sesion</h5>
            <q-input v-model="correo" rounded outlined class="q-mb-lg" placeholder="ejemplo@gmail.com" type="email" label="correo"/>
            <q-input v-model="pass" rounded outlined :type="isPwd ? 'password' : 'text'" label="contraseña">
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
          </q-card-section>
          <q-separator/>
          <q-card-actions vertical align="around">
            <q-btn color="primary" class="q-mb-md" label="Iniciar sesion" @click="makeLogin"/>
            <q-btn flat text-color="primary" label="Contactar al desarrollador" @click="showContactForm"/>
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { Loading, Notify, Dialog } from 'quasar'
import { validation } from 'boot/axios'
import CryptoJS from 'crypto-js'
import contactMe from 'components/contactForm.vue'

export default {
  name: 'login',
  methods: {
    makeLogin () {
      const data = { // eslint-disable-next-line
          "user": { // eslint-disable-next-line
            "email": this.correo, // eslint-disable-next-line
            "pass": CryptoJS.MD5(this.pass).toString()
        }
      }
      Loading.show({
        message: 'Iniciando sesion',
        boxClass: 'bg-grey-2 text-primary'
      })
      validation.post(
        '/login',
        data
      ).then((res) => {
        Loading.hide()
        Notify.create({
          type: 'positive',
          message: 'Sesion iniciada correctamente',
          textColor: 'dark',
          timeout: 1000
        })
        const user = res.data.user
        const token = res.data.JWT
        this.store.dispatch('currentUser/saveTokenAction', { token })
        this.store.dispatch('currentUser/saveUserAction', { user })
        this.$router.push('/h')
      }).catch((err) => {
        if (err.message.includes('404')) {
          Notify.create({
            type: 'negative',
            message: 'Usuario y/o contraseña invalidos'
          })
        } else {
          console.log(err)
          Notify.create({
            type: 'negative',
            message: 'No se pudo iniciar sesion'
          })
        }
        Loading.hide()
      })
    },

    showContactForm () {
      Dialog.create({
        component: contactMe
      })
    }
  },

  setup () {
    const correo = ref('')
    const pass = ref('')
    const isPwd = ref(true)
    const store = useStore()

    return {
      correo,
      pass,
      isPwd,
      store
    }
  }
}
</script>
