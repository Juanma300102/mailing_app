<template>
  <q-layout dark view="hhh Lpr lFf">
    <q-header>
      <q-toolbar class="light-dark">
        <q-toolbar-title>Mailing App</q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="drawer"
      show-if-above
      :mini="mini"
      @mouseover="mini = false"
      @mouseout="mini = true"
    >
      <q-scroll-area class="fit">
        <q-list padding>
          <q-item clickable v-ripple>
            <q-item-section avatar class="q-mb-sm">
              <q-btn round flat class="bg-primary">{{ firstLettersUserName }}</q-btn>
            </q-item-section>
            <q-item-section>
              <div class="col">
                <div class="row text-h6">
                  {{ this.userName }}
                </div>
                <div class="row text-caption">
                  {{ this.userEmail }}
                </div>
              </div>
            </q-item-section>
          </q-item>
          <q-separator/>
          <leftMenuItem label="Principal" icon="home" routerPath="/h"/>
          <leftMenuItem label="Borradores hechos" icon="drafts" routerPath="/h"/>
          <leftMenuItem label="Envio de correos" icon="send" routerPath="/h"/>
          <q-separator/>
          <q-item dense clickable v-ripple @click="switchTeme()">
            <q-item-section avatar>
              <q-icon :name=" this.dark ? 'toggle_on' : 'toggle_off'"/>
            </q-item-section>
            <q-item-section>
              Tema Oscuro
            </q-item-section>
          </q-item>
          <leftMenuItem dense label="Cerrar sesión" icon="logout" routerPath="/" @click="logout()"/>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { Cookies, Notify } from 'quasar'
import { validation } from 'boot/axios'
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import leftMenuItem from 'components/leftMenuItem.vue'

export default defineComponent({
  name: 'MainLayout',

  components: {
    leftMenuItem
  },

  data () {
    return {
      drawer: true,
      mini: true,
      dark: true
    }
  },

  computed: {
    firstLettersUserName () {
      const user = this.$q.cookies.has('currentUser') ? this.$q.cookies.get('currentUser') : ''
      const name = `${user.nombre}`
      let initials = ''
      name.split(' ').forEach(word => {
        initials += word[0]
      })
      return initials
    },

    userName () {
      return this.store.getters['currentUser/getCurrentUserName']
    },

    userEmail () {
      return this.store.getters['currentUser/getCurrentUserEmail']
    }
  },

  methods: {
    logout () {
      Cookies.remove('currentUser')
      Cookies.remove('sessionToken')
      this.$q.notify({
        type: 'info',
        message: 'Sesión cerrada correctamente',
        timeout: 1000,
        textColor: 'dark'
      })
    },
    switchTeme () {
      this.dark = !this.dark
      this.$q.dark.set(this.dark)
    }
  },

  setup () {
    const router = useRouter()
    const store = useStore()
    if (Cookies.has('sessionToken')) {
      validation.post('/verify_token', {}, {
        headers: {
          Authorization: `Bearer ${Cookies.get('sessionToken')}`
        }
      })
        .then(() => {
          store.dispatch('currentUser/saveUserAction',
            {
              user: Cookies.has('currentUser') ? Cookies.get('currentUser') : null
            })
          store.dispatch('currentUser/saveTokenAction',
            {
              token: Cookies.has('sessionToken') ? Cookies.get('sessionToken') : null
            })
        }
        )
        .catch(() => {
          Notify.create({
            type: 'info',
            message: 'Sesión expirada',
            timeout: 2000
          })
          router.push('/')
        })
    } else {
      Notify.create({
        type: 'warning',
        message: 'Debes iniciar sesión',
        timeout: 2000
      })
      router.push('/')
    }
    return {
      store
    }
  }
})
</script>
