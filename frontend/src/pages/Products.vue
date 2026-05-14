<template>
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="Products" />
    </template>
    <template #right-header>
      <CustomActions
        v-if="productsListView?.customListActions"
        :actions="productsListView.customListActions"
      />
      <Button
        variant="solid"
        :label="__('Create')"
        iconLeft="plus"
        @click="showProductModal = true"
      />
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="products"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="CRM Product"
  />
  <ProductsListView
    v-if="products.data && rows.length"
    ref="productsListView"
    v-model="products.data.page_length_count"
    v-model:list="products"
    :rows="rows"
    :columns="columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: products.data.row_count,
      totalCount: products.data.total_count,
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @applyFilter="(data) => viewControls.applyFilter(data)"
    @applyLikeFilter="(data) => viewControls.applyLikeFilter(data)"
    @likeDoc="(data) => viewControls.likeDoc(data)"
    @selectionsChanged="
      (selections) => viewControls.updateSelections(selections)
    "
  />
  <EmptyState
    v-else-if="products.data && !rows.length"
    name="Products"
    :icon="ProductsIcon"
  />
  <ProductModal
    v-if="showProductModal"
    v-model="showProductModal"
  />
</template>

<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import CustomActions from '@/components/CustomActions.vue'
import ProductsIcon from '@/components/Icons/ProductsIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ProductModal from '@/components/Modals/ProductModal.vue'
import ProductsListView from '@/components/ListViews/ProductsListView.vue'
import EmptyState from '@/components/ListViews/EmptyState.vue'
import ViewControls from '@/components/ViewControls.vue'
import { getMeta } from '@/stores/meta'
import { formatDate, timeAgo } from '@/utils'
import { ref, computed } from 'vue'

const { getFormattedPercent, getFormattedFloat, getFormattedCurrency } =
  getMeta('CRM Product')

const productsListView = ref(null)
const showProductModal = ref(false)

// products data is loaded in the ViewControls component
const products = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

const rows = computed(() => {
  if (!products.value?.data?.data) return []
  const viewType = products.value.data.view_type
  if (viewType && !['list', 'group_by'].includes(viewType)) return []
  return products.value.data.data.map((product) => {
    let _rows = { name: product.name }
    products.value.data.rows.forEach((row) => {
      _rows[row] = product[row]

      let fieldType = products.value.data.columns?.find(
        (col) => (col.key || col.value) == row,
      )?.type

      if (
        fieldType &&
        ['Date', 'Datetime'].includes(fieldType) &&
        !['modified', 'creation'].includes(row)
      ) {
        _rows[row] = formatDate(
          product[row],
          '',
          true,
          fieldType == 'Datetime',
        )
      }

      if (fieldType && fieldType == 'Currency') {
        _rows[row] = getFormattedCurrency(row, product)
      }

      if (fieldType && fieldType == 'Float') {
        _rows[row] = getFormattedFloat(row, product)
      }

      if (fieldType && fieldType == 'Percent') {
        _rows[row] = getFormattedPercent(row, product)
      }

      if (['modified', 'creation'].includes(row)) {
        _rows[row] = {
          label: formatDate(product[row]),
          timeAgo: __(timeAgo(product[row])),
        }
      }
    })
    return _rows
  })
})

const columns = computed(() => {
  let _columns = products.value?.data?.columns || []

  if (_columns.length) {
    _columns = _columns.map((col, index) => {
      if (index === _columns.length - 1) {
        return { ...col, align: 'right' }
      }
      return col
    })
  }

  return _columns
})
</script>
