<template>
  <n-data-table :columns="columns" :data="data" :pagination="pagination" />
</template>

<script lang="ts">
import { defineComponent, h } from 'vue'
import { useRouter } from "vue-router";
import type { DataTableColumns } from 'naive-ui'
import { NButton, NTag, useMessage } from 'naive-ui'

interface RowData {
  key: number
  patient: string
  type: string
  type_label: string,
  timeCreated: string,
  timeUpdated: string,
  status: string
}

function createColumns(router): DataTableColumns<RowData> {
  return [
    /* {
      type: 'selection'
    },
    {
      type: 'expand',
      expandable: rowData => rowData.status === 'pending',
      renderExpand: (rowData) => {
        return `${rowData?.status_details}`
      }
    }, */
    /* {
      title: '#',
      key: 'key',
      render: (_, index) => {
        return `${index + 1}`
      }
    }, */
    {
      title: 'Pacient',
      key: 'patient'
    },
    {
      title: 'Druh žádosti',
      key: 'type_label'
    },
    {
      title: 'Čas vytvoření',
      key: 'timeCreated'
    },
    {
      title: 'Čas poslední úpravy',
      key: 'timeUpdated'
    },
    {
      title: 'Status',
      key: 'status'
    },
    {
      title: '',
      key: 'actions',
      render(row) {
        return h(
          NButton,
          {
            size: 'small',
            onClick: () => router.push(`zadosti/${row.key}`)
          },
          { default: () => 'Detail' }
        )
      }
    }
  ]
}

function createData(): RowData[] {
  return [
  {
      "key": 0,
      "patient": "Jana Malá",
      "type": "Prescription",
      "type_label": "Male",
      "timeCreated": "2021-09-14T14:00:00",
      "timeUpdated": "2021-09-14T14:00:00",
      "status": "Pending",
    }
  ]
}

export default defineComponent({
  setup() {
    const message = useMessage();
    const router = useRouter();
    return {
      data: createData(),
      columns: createColumns(router),
      pagination: {
        pageSize: 10
      }
    }
  }
})
</script>