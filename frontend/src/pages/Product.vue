<template>
  <LayoutHeader v-if="product.doc">
    <template #left-header>
      <Breadcrumbs
        :items="[
          { label: __('Products'), route: { name: 'Products' } },
          { label: product.doc.product_name || product.doc.product_code || productId },
        ]"
      />
    </template>
    <template #right-header>
      <CustomActions
        v-if="product._actions?.length"
        :actions="product._actions"
      />
      <Button
        v-if="isManager() && !isMobileView"
        variant="ghost"
        class="w-7"
        :tooltip="__('Edit Fields Layout')"
        :icon="EditIcon"
        @click="openQuickEntryModal"
      />
      <Button
        variant="solid"
        :label="__('Save')"
        :loading="product.save?.loading"
        @click="saveProduct"
      />
    </template>
  </LayoutHeader>
  <div
    v-if="product.doc"
    class="flex flex-1 flex-col overflow-y-auto p-6"
  >
    <div class="mx-auto w-full max-w-3xl">
      <FieldLayout
        v-if="tabs.data?.length"
        :tabs="tabs.data"
        :data="product.doc"
        doctype="CRM Product"
      />
      <ErrorMessage v-if="error" class="mt-4" :message="__(error)" />
    </div>
  </div>
</template>

<script setup>
import EditIcon from '@/components/Icons/EditIcon.vue'
import FieldLayout from '@/components/FieldLayout/FieldLayout.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import CustomActions from '@/components/CustomActions.vue'
import { usersStore } from '@/stores/users'
import { isMobileView } from '@/composables/settings'
import { showQuickEntryModal, quickEntryProps } from '@/composables/modals'
import { useDocument } from '@/data/document'
import { createResource, toast } from 'frappe-ui'
import { Breadcrumbs } from 'frappe-ui'
import { ref, nextTick } from 'vue'

const props = defineProps({
  productId: { type: String, required: true },
})

const { isManager } = usersStore()
const error = ref(null)

const { document: product, triggerOnBeforeCreate } = useDocument(
  'CRM Product',
  props.productId,
)

async function saveProduct() {
  error.value = null
  try {
    await product.save.submit()
    toast({ title: __('Product saved'), variant: 'success' })
  } catch (err) {
    error.value = err?.messages?.[0] || err?.message
  }
}

const tabs = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_fields_layout',
  cache: ['QuickEntry', 'CRM Product'],
  params: { doctype: 'CRM Product', type: 'Quick Entry' },
  auto: true,
})

function openQuickEntryModal() {
  showQuickEntryModal.value = true
  quickEntryProps.value = { doctype: 'CRM Product' }
}
</script>
