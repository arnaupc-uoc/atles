export default {
  props: {
    actions: { type: Array, required: true }
  },
  emits: ['action-click'],
  template: `
    <div class="d-flex ga-2 justify-center">
      <v-tooltip
        v-for="action in actions"
        :key="action.name"
        location="top"
      >
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            icon
            variant="tonal"
            size="small"
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
