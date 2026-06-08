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
      tableSearch: '',
      pagination: {
        page: this.page,
        rowsPerPage: this.options.rowsPerPage || Math.max(1, Math.ceil(this.total / Math.max(this.totalPages, 1))),
        rowsNumber: this.total
      }
    };
  },
  computed: {
    searchEnabled() { return this.options.search || false; },
    searchLabel() { return this.options.search_label || 'Cerca a la taula'; },
    density() {
      if (this.options.dense && !this.options.density) return 'comfortable';
      return this.options.density || 'comfortable';
    },
    tableHeight() { return this.options.height || null; },
    computedHeaders() {
      const headers = this.columns.map(col => ({
        name: col.key,
        label: col.label,
        field: col.key,
        sortable: true
      }));
      if (this.rows.length > 0 && this.rows[0].actions !== undefined) {
        headers.push({ name: 'actions', label: 'Accions', field: 'actions', sortable: false, align: 'center' });
      }
      return headers;
    }
  },
  watch: {
    page(newPage) {
      if (this.pagination.page !== newPage) {
        this.pagination.page = newPage;
      }
    },
    total(newTotal) {
      this.pagination.rowsNumber = newTotal;
    },
    totalPages(newTotalPages) {
      this.pagination.rowsPerPage = this.options.rowsPerPage || Math.max(1, Math.ceil(this.total / Math.max(newTotalPages, 1)));
    },
    'pagination.page'(newPage) {
      this.updatePage(newPage);
    }
  },
  methods: {
    updatePage(newPage) {
      if (newPage === this.page) return;

      const url = new URL(this.endpointUrlBase, window.location.origin);
      url.searchParams.set('page', newPage);
      Object.entries(this.filters).forEach(([key, val]) => {
        if (val !== null && val !== undefined && val !== '') {
          url.searchParams.set(key, val);
        }
      });
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
      <div class="row q-gutter-md mb-4" v-if="searchEnabled">
        <div class="col-12 col-md-4">
          <q-input
            v-model="tableSearch"
            :label="searchLabel"
            clearable
            append-icon="search"
            dense
          />
        </div>
      </div>

      <q-table
        :columns="computedHeaders"
        :rows="rows"
        row-key="id"
        :pagination.sync="pagination"
        :filter="searchEnabled ? tableSearch : ''"
        flat
        dense
      >
        <template v-slot:body-cell-actions="props">
          <admin-table-actions
            :actions="props.row.actions"
            @action-click="handleAction"
          />
        </template>
      </q-table>
    </div>
  `
};
