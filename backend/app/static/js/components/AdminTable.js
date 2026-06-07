// Importem el subcomponent des del seu fitxer
import AdminTableActions from './AdminTableActions.js';

export default {
  components: {
    AdminTableActions
  },
  props: {
    columns: { type: Array, required: true },
    rows: { type: Array, required: true },
    page: { type: Number, required: true },
    total: { type: Number, required: true },
    totalPages: { type: Number, required: true },
    endpointUrlBase: { type: String, required: true },
    filters: { type: Object, default: () => ({}) },
    options: { type: Object, default: () => ({}) }
  },
  emits: ['action-click'],
  data() {
    return {
      tableSearch: ''
    };
  },
  computed: {
    searchEnabled() { return this.options.search || false; },
    searchLabel() { return this.options.search_label || 'Cerca a la taula'; },
    density() {
      if (this.options.dense && !this.options.density) return 'compact';
      return this.options.density || null;
    },
    sortBy() { return this.options.sort_by || null; },
    sortDesc() { return this.options.sort_desc || false; },
    tableHeight() { return this.options.height || null; },

    // Maqueta els headers incloent les accions si cal
    computedHeaders() {
      const headers = this.columns.map(col => ({
        title: col.label,
        key: col.key
      }));
      if (this.rows.length > 0 && this.rows[0].actions !== undefined) {
        headers.push({ title: 'Accions', key: 'actions', sortable: false, align: 'center' });
      }
      return headers;
    }
  },
  methods: {
    // Escolta el canvi de pàgina de la barra nativa de Vuetify
    updatePage(newPage) {
      // Si la pàgina coincideix amb l'actual, no fem res (evita bucles)
      if (newPage === this.page) return;

      const url = new URL(this.endpointUrlBase, window.location.origin);
      url.searchParams.set('page', newPage);

      // Afegim els filtres existents a la URL
      Object.entries(this.filters).forEach(([key, val]) => {
        if (val !== null && val !== undefined && val !== '') {
          url.searchParams.set(key, val);
        }
      });

      // Redirigim a la nova pàgina de Flask
      window.location.href = url.pathname + url.search;
    },
    handleAction(action) {
      this.$emit('action-click', {
        label: action.label,
        message: `Estàs segur que vols ${action.label.toLowerCase()}?`,
        href: action.href
      });
    }
  },
  template: `
    <div>
      <v-row class="g-4 mb-4" v-if="searchEnabled">
        <v-col cols="12" md="4">
          <v-text-field
            v-model="tableSearch"
            :label="searchLabel"
            clearable
            append-inner-icon="mdi-magnify"
            density="comfortable"
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>

      <v-data-table-server
        :headers="computedHeaders"
        :items="rows"
        :items-length="total"
        :page="page"
        class="border-sm"
        :density="density"
        :search="searchEnabled ? tableSearch : ''"
        :height="tableHeight"
        @update:page="updatePage"
      >
        <template #item.actions="{ item }">
          <admin-table-actions
            :actions="item.actions"
            @action-click="handleAction"
          ></admin-table-actions>
        </template>
      </v-data-table-server>
    </div>
  `
};
