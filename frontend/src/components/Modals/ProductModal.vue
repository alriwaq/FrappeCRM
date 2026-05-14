<template>
  <Dialog v-model="show" :options="{ size: 'xl' }">
    <template #body>
      <div class="px-4 pt-5 pb-6 bg-surface-modal sm:px-6">
        <div class="flex items-center justify-between mb-5">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ __('New Product') }}
            </h3>
          </div>
          <div class="flex items-center gap-1">
            <Button
              v-if="isManager() && !isMobileView"
              variant="ghost"
              class="w-7"
              :tooltip="__('Edit Fields Layout')"
              :icon="EditIcon"
              @click="openQuickEntryModal"
            />
            <Button
              variant="ghost"
              class="w-7"
              icon="x"
              @click="show = false"
            />
          </div>
        </div>
        <FieldLayout
          v-if="tabs.data?.length"
          :tabs="tabs.data"
          :data="product.doc"
          doctype="CRM Product"
        />
        <ErrorMessage v-if="error" class="mt-4" :message="__(error)" />
      </div>
      <div class="px-4 pt-4 pb-7 sm:px-6">
        <div class="flex flex-row-reverse gap-2">
          <Button
            variant="solid"
            :label="__('Create')"
            :loading="_create.loading"
            @click="createProduct"
          />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import EditIcon from '@/components/Icons/EditIcon.vue'
import FieldLayout from '@/components/FieldLayout/FieldLayout.vue'
import { usersStore } from '@/stores/users'
import { isMobileView } from '@/composables/settings'
import { showQuickEntryModal, quickEntryProps } from '@/composables/modals'
import { useDocument } from '@/data/document'
import { createResource } from 'frappe-ui'
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  defaults: { type: Object, default: () => ({}) },
})

const show = defineModel({ type: Boolean })

const { isManager } = usersStore()
const router = useRouter()
const error = ref(null)

const { document: product, triggerOnBeforeCreate } = useDocument('CRM Product')

const _create = createResource({
  url: 'frappe.client.insert',
  onSuccess: (d) => {
    product.doc = {}
    show.value = false
    router.push({ name: 'Product', params: { productId: d.name } })
  },
  onError: (err) => {
    if (err.exc_type == 'MandatoryError') {
      const fieldName = err.messages
        .map((msg) => {
          let arr = msg.split(': ')
          return arr[arr.length - 1].trim()
        })
        .join(', ')
      error.value = __('Please fill the mandatory fields: {0}', [fieldName])
      return
    }
    error.value = err.messages?.[0] || __('Could not create product')
  },
})

async function createProduct() {
  error.value = null
  await triggerOnBeforeCreate?.()
  _create.submit({
    doc: {
      doctype: 'CRM Product',
      ...product.doc,
    },
  })
}

const tabs = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_fields_layout',
  cache: ['QuickEntry', 'CRM Product'],
  params: { doctype: 'CRM Product', type: 'Quick Entry' },
  auto: true,
})

onMounted(() => {
  product.doc = {
    ...product.doc,
    ...props.defaults,
  }
})

function openQuickEntryModal() {
  showQuickEntryModal.value = true
  quickEntryProps.value = { doctype: 'CRM Product' }
  nextTick(() => (show.value = false))
}
</script>
