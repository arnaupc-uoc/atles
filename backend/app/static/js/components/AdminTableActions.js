export default {
  props: {
    actions: { type: Array, required: true }
  },
  emits: ['action-click'],
  methods: {
    onActionClick(event, action) {
      if (event && event.currentTarget) {
        event.currentTarget.blur();
      }
      this.$emit('action-click', action);
    }
  },
  template: `
    <div class="row items-center justify-center q-gutter-sm">
      <div v-for="action in actions" :key="action.name">
        <q-btn
          dense
          flat
          round
          :icon="action.icon"
          @click="onActionClick($event, action)"
        >
          <q-tooltip anchor="top middle">{{ action.label }}</q-tooltip>
        </q-btn>
      </div>
    </div>
  `
};
