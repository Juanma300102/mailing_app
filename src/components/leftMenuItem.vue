<template>
  <q-item clickable v-ripple @click="goTo(routerPath)" class="q-my-md">
    <q-item-section avatar>
      <q-icon :name="icon"/>
    </q-item-section>
    <q-item-section>
      {{ label }}
    </q-item-section>
  </q-item>
</template>

<script>
export default {
  name: 'leftMenuItem',

  props: {
    icon: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    routerPath: {
      type: String,
      required: true
    }
  },
  methods: {
    goTo (route) {
      this.$router.push(route)
    }
  }
}
</script>
