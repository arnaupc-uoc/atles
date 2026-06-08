export default {
  props: {
    modelValue: { type: Boolean, required: true },
    title: { type: String, default: '' },
    message: { type: String, default: '' },
    hasAction: { type: Boolean, default: false }
  },
  emits: ['update:modelValue', 'confirm'],
  computed: {
    isOpen: {
      get() { return this.modelValue; },
      set(value) { this.$emit('update:modelValue', value); }
    }
  },
  template: `
    <q-dialog
      v-model="isOpen"
      transition-show="slide-up"
      transition-hide="slide-down"
      persistent
    >
      <q-card class="bg-white q-pa-md" style="min-width: 320px; max-width: 640px;">
        <q-btn
          dense
          flat
          round
          icon="close"
          @click="isOpen = false"
          class="absolute-top-right q-mr-md q-mt-md"
        />

        <q-card-section class="q-pt-xl q-px-lg q-pb-lg">
          <div class="text-h5 q-mb-md">{{ title }}</div>

          <div v-if="message" class="q-mb-lg" style="white-space: pre-line;">
            {{ message }}
          </div>

          <div v-if="hasAction" class="row q-gutter-sm">
            <q-btn
              color="primary"
              unelevated
              label="Confirmar"
              @click="$emit('confirm')"
            />
            <q-btn
              flat
              label="Cancelar"
              @click="isOpen = false"
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  `
};
