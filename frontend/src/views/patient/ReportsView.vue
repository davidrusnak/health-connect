<template>
  <div class="max-w-4xl ml-auto mr-auto lg:relative lg:-left-36">
    <Card>
      <template #header><h3>Zpráva</h3></template>
      <div style="line-height: normal;" v-html="report_example_html"></div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import report_example from "@/data/report-example"

const report_example_html = report_example.replace(/\n/g, '<br>')

</script>