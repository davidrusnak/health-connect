<template>
  <section class="max-w-lg">
    <n-form ref="formRef" :model="formValue" :rules="rules" :validate-messages="messages">
      <div class="flex flex-row items-center space-x-4 justify-items-stretch w-full min-w-full max-w-full">
        <n-form-item label="Název edukačního materiálu" path="user.name">
          <n-input v-model:value="formValue.name" placeholder="Název" />
        </n-form-item>
        <n-button type="primary" @click="handleValidateClick">
          Uložit
        </n-button>
      </div>
    </n-form>
  </section>

  <div class="max-w-7xl">
    <EduResourceEditor v-model="editorContent" />
  </div>
</template>

<script setup lang="ts">
import { type FormInst, useMessage } from 'naive-ui';
import { ref } from 'vue';

const formRef = ref<FormInst | null>(null)
const message = useMessage();

const editorContent = ref('<h1>YESSS</h1>');

const formValue = ref({
  name: ''
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
