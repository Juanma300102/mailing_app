<template>
  <q-layout dark view="lhh Lpr lFf">
    <q-header>
      <q-toolbar class="light-dark">
        <q-btn flat round icon="menu" dense @click="toggleLeftDrawer"/>
        <q-toolbar-title>Mailing App</q-toolbar-title>
        <q-btn round flat class="bg-accent">{{ firstLettersUserName }}</q-btn>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      class="bg-secondary"
    >
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

export default defineComponent({
  name: 'MainLayout',

  data () {
    return {
      leftDrawerOpen: false
    }
  },

  computed: {
    firstLettersUserName () {
      const user = this.$q.cookies.get('currentUser')
      const name = `${user.nombre} ${user.apellido}`
      let initials = ''
      name.split(' ').forEach(word => {
        initials += word[0]
      })
      return initials
    }
  },

  methods: {
    toggleLeftDrawer () {
      this.leftDrawerOpen = !this.leftDrawerOpen
    }
  },

  setup () {
    const $router = useRouter()
    const $store = useStore()
    if (Cookies.has('sessionToken')) {
      validation.post('/verify_token', {}, {
        headers: {
          Authorization: `Bearer ${Cookies.get('sessionToken')}`
        }
      })
        .catch(() => {
          Notify.create({
            type: 'info',
            message: 'Sesión expirada',
            timeout: 2000
          })
          $router.push('/')
        })
    } else {
      Notify.create({
        type: 'warning',
        message: 'Debes iniciar sesión',
        timeout: 2000
      })
      $router.push('/')
    }
    return {
      $store
    }
  }
})
</script>
