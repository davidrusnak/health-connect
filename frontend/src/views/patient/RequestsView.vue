<template>
  <div v-auto-animate>
    <div v-if="request_state === 'openable'">
      <Button label="Nová žádost na lékaře" @click="request_state = 'open_set_type'"></Button>
    </div>

    <div v-else-if="request_state === 'open_set_type'" class="grid space-y-2">
      <h3>O co chcete požádat?</h3>
      <div v-for="t in request_types" :key="t.key">
        <Button :label="t.label"
          @click="request_state = 'open_set_doctor'; request.type = t.key; request.type_desc = t.desc; request.type_label = t.label"></Button>
      </div>
    </div>

    <div v-else-if="request_state === 'open_set_doctor'">
      <h3>Žádost odešlete doktorovi:</h3>
      <div class="flex flex-row items-start w-64 space-x-3 mb-6">
        <img class="w-12 rounded-full" src="/dusek.jpeg" alt="Lékař">
        <div class="flex flex-col space-y-1 mt-1.5">
          <span class="font-bold">MUDr. Vítězslav Dušek</span>
          <span>Klinika detské onkologie</span>
        </div>
      </div>
      <div class="mt-4 flex flex-row space-x-2"><Button back @click="request_state = 'open_set_type'" /><Button
          label="Dále" @click="request_state = 'filling'" /></div>
    </div>

    <div v-else-if="request_state === 'filling'" class="w-full lg:max-w-lg">
      <h2 class="mx-2">Nová žádanka: {{ request.type_label }}</h2>

      <div class="flex flex-col">
        <n-input placeholder="Napište název léku." autosize maxlength="50" show-count size="large"
          v-model:value="request.drug_name" />
        <div class="mt-2"><n-input placeholder="Jestli máte k předpisu dotaz, vyplňte zde." maxlength="100" show-count
            type="textarea" size="large" :autosize="{
      minRows: 3,
      maxRows: 5,
    }" v-model:value="request.text" /></div>
        <div class="mt-4 flex flex-row space-x-2"><Button back @click="request_state = 'open_set_doctor'" /><Button
            label="Dále" @click="request_state = 'check_before_send'" /></div>
      </div>
    </div>

    <div v-else-if="request_state === 'check_before_send'">
      <h3>Je vaše žádost v pořádku?</h3>
      <div class="max-w-lg">
        <n-descriptions label-placement="top" title="" size="large">
          <n-descriptions-item>
            <template #label>

              Žádost o
            </template>{{ request.type_label }}
          </n-descriptions-item>
          <n-descriptions-item>
            <template #label>
              Doktor
            </template>
            {{ request.doctor }}
          </n-descriptions-item>
          <n-descriptions-item>
            <template #label>
              Text zprávy
            </template>
            {{ request.text }}
          </n-descriptions-item>
        </n-descriptions>
      </div>
      <div class="mt-4"><Button label="Odeslat" @click="request_state = 'sending'"></Button></div>
    </div>

    <div v-else-if="request_state === 'sending'">
      <h3>Odesílám žádost...</h3>
    </div>

    <div v-else-if="request_state === 'sent'">
      <h3>Žádost úspěšně podaná. Odpověď vám dáme vědet emailem a SMS.</h3>
      <Button label="OK" @click="request_state = 'openable'"></Button>
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref } from 'vue';

const checkedValueRef = ref<string | null>(null);

/**
 * openable - user can create new request
 * open_set_type - user is selecting the type of request
 * open_set_doctor - user is selecting the doctor
 * filling - user is filling the request
 * check_before_send
 * sending - request is being sent
 * sent - request has been sent
 */
const request_state = ref("openable");

// 'drug-prescription', 'request-appointment', 'upload-external-report', 'general-request'
const request_types = [
  { key: 'drug-prescription', label: 'Recept na léky', desc: 'Požádat o recept na léky', icon: 'drug' },
  { key: 'request-appointment', label: 'Objednání na vyšetření', desc: '', icon: 'calendar' },
  { key: 'upload-external-report', label: 'Nahrát externí zprávu', desc: 'Nahrát zprávu od jiného lékaře', icon: 'file' },
  { key: 'general-request', label: 'Obecná žádost', desc: 'Vytvořit obecnou žádost', icon: 'question' },
];

const request = ref({
  type: '',
  type_label: '',
  type_desc: '',
  doctor: 'MUDr. Vítězslav Dušek',
  text: '',
  drug_name: '',
  attachments: [],
});

</script>