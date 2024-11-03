<template>
  <div class="flex flex-row space-x-16">
    <div class="max-w-7xl w-full h-full min-h-100">
      <EduResourceEditor v-model="editorContent" />
    </div>

    <section class="max-w-lg">
      <n-form ref="formRef" :model="formValue" :rules="rules" :validate-messages="messages">
        <div class="flex flex-col items-start justify-items-stretch w-full min-w-full max-w-full">
          <n-form-item label="Název edukačního materiálu" path="nazev">
            <n-input v-model:value="formValue.name" placeholder="Název" />
          </n-form-item>
          <n-button type="primary" @click="handleValidateClick">
            Uložit
          </n-button>
        </div>
      </n-form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { type FormInst, useMessage } from 'naive-ui';
import { onMounted, ref } from 'vue';

const formRef = ref<FormInst | null>(null)
const message = useMessage();
const editorContent = ref();
const formValue = ref({
  name: ''
})

onMounted(() => {
  editorContent.value = '<h1>YESSS</h1>';
})

const messages = {
  required: 'Pole "%s" je vyžadováno.'
}
const rules = {
  user: {
    name: {
      required: true,
      trigger: 'blur'
    }
  }
}

function handleValidateClick(e: MouseEvent) {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      message.success('Uloženo')
    }
    else {
      console.log(errors)
      message.error('Před uložením zvolte meno')
    }
  })
}
</script>

<style>
.ck.ck-content.ck-editor__editable {
  height: 76vh;
}
</style>
