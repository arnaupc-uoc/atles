export default {
  props: {
    actions: { type: Array, required: true }
  },
  emits: ['action-click'],
  methods: {
    onActionClick(event, action) {
      // Forcem el desforç (blur) del botó actiu perquè perdi l'estat "marcat" immediatament
      if (event && event.currentTarget) {
        event.currentTarget.blur();
      }

      // Emetem l'esdeveniment cap al pare com fins ara
      this.$emit('action-click', action);
    }
  },
  template: `
    <div class="d-flex ga-2 justify-center">
      <v-tooltip
        v-for="action in actions"
        :key="action.name"
        location="top"
        :open-on-click="false"
        :open-on-focus="false"
        eager
      >
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            icon
            variant="tonal"
            size="small"
            density="comfortable"
            @click="$emit('action-click', action)"
          >
            <v-icon size="small">{{ action.icon }}</v-icon>
          </v-btn>
        </template>
        <span>{{ action.label }}</span>
      </v-tooltip>
    </div>
  `
};
