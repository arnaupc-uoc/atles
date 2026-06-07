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
    <v-dialog
      v-model="isOpen"
      fullscreen
      transition="dialog-bottom-transition"
    >
      <v-card class="bg-white opacity-90 rounded-0 position-relative">

        <v-btn
          icon="mdi-close"
          variant="text"
          @click="isOpen = false"
          class="position-absolute top-0 right-0 ma-4"
          style="z-index: 10;"
        ></v-btn>

        <v-container class="fill-height d-flex align-center justify-center pa-6" style="max-width: 1280px;">
          <div class="w-100">

            <div class="pb-4 mb-4 border-b">
              <h2 class="text-h4 font-weight-bold">{{ title }}</h2>
            </div>

            <div>
              <p v-if="message" class="text-body-1 mb-6 text-grey-darken-3" style="white-space: pre-line;">
                {{ message }}
              </p>

              <div v-if="hasAction" class="d-flex ga-3">
                <v-btn
                  color="primary"
                  size="large"
                  @click="$emit('confirm')"
                >
                  Confirmar
                </v-btn>
                <v-btn
                  variant="tonal"
                  size="large"
                  @click="isOpen = false"
                >
                  Cancelar
                </v-btn>
              </div>
            </div>

          </div>
        </v-container>
      </v-card>
    </v-dialog>
  `
};
