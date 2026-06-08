export default {
  props: {
    fields: { type: Array, required: true },
    endpointUrl: { type: String, required: true },
    initialFilters: { type: Object, default: () => ({}) },
    method: { type: String, default: 'get' }
  },
  data() {
    return {
      showFilters: false,
      filters: { ...this.initialFilters }
    };
  },
  template: `
    <div class="mb-6">
      <q-btn
        color="primary"
        unelevated
        :icon="showFilters ? 'search_off' : 'search'"
        @click="showFilters = !showFilters"
        class="mb-4"
        :label="showFilters ? 'Amagar Cercador' : 'Buscador'"
      />

      <form :method="method" v-if="showFilters">
        <div class="row q-gutter-md">
          <div v-for="field in fields" :key="field.name" class="col-12 col-md-4">
            <q-select
              v-if="field.options"
              :name="field.name"
              :label="field.label"
              :options="field.options"
              option-label="label"
              option-value="value"
              v-model="filters[field.name]"
              clearable
            />

            <q-input
              v-else
              :name="field.name"
              :label="field.label"
              v-model="filters[field.name]"
              clearable
            />
          </div>
        </div>

        <div class="row q-gutter-sm q-mt-md">
          <div class="col-auto">
            <q-btn color="primary" unelevated type="submit" label="Filtrar" />
            <q-btn flat color="secondary" :href="endpointUrl" label="Netejar" class="q-ml-sm" />
          </div>
        </div>
      </form>
    </div>
  `
};
