export default {
  props: {
    fields: { type: Array, required: true },
    endpointUrl: { type: String, required: true },
    initialFilters: { type: Object, default: () => ({}) },
    method: { type: String, default: 'get' }
  },
  data() {
    return {
      showFilters: false, // Estat aïllat
      filters: { ...this.initialFilters }
    };
  },
  template: `
    <div class="mb-6">
      <v-btn
        color="primary"
        :prepend-icon="showFilters ? 'mdi-magnify-minus' : 'mdi-magnify'"
        @click="showFilters = !showFilters"
        class="mb-4"
      >
        {{ showFilters ? 'Amagar Cercador' : 'Buscador' }}
      </v-btn>

      <form :method="method" v-if="showFilters">
        <v-row class="g-4">
          <v-col v-for="field in fields" :key="field.name" cols="12" md="4">

            <v-select
              v-if="field.options"
              :name="field.name"
              :label="field.label"
              :items="field.options"
              item-title="label"
              item-value="value"
              v-model="filters[field.name]"
              clearable
            ></v-select>

            <v-text-field
              v-else
              :name="field.name"
              :label="field.label"
              v-model="filters[field.name]"
              clearable
            ></v-text-field>

          </v-col>
        </v-row>

        <v-row class="g-4 mt-0">
          <v-col cols="auto" class="d-flex ga-2">
            <v-btn color="primary" type="submit">Filtrar</v-btn>
            <v-btn variant="tonal" color="secondary" :href="endpointUrl">Netejar</v-btn>
          </v-col>
        </v-row>
      </form>
    </div>
  `
};
