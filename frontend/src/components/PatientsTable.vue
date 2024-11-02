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
  name: string
  age: number
  sex: string,
  tags: string[],
  status: string,
  status_details?: string
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
      title: 'Jméno',
      key: 'name'
    },
    {
      title: 'Věk',
      key: 'age'
    },
    {
      title: 'Biologické pohlaví',
      key: 'sex'
    },
    /* {
      title: 'Tags',
      key: 'tags',
      render(row) {
        const tags = row.tags.map((tagKey) => {
          return h(
            NTag,
            {
              style: {
                marginRight: '6px'
              },
              type: 'info',
              bordered: false
            },
            {
              default: () => tagKey
            }
          )
        })
        return tags
      }
    }, */
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
            onClick: () => router.push(`pacienti/${row.key}`)
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
      key: 0,
      "name": "Mustafa Abrahim",
      "age": 34,
      "sex": "M",
      "status": "Žádné upozornění",
      tags: []
    },
    {
      key: 1,
      "name": "Mustafa Abrahim",
      "age": 34,
      "sex": "M",
      "status": "Žádné upozornění",
      tags: []
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