<template>
    <div class="table-content">
        <el-tabs>
            <el-tab-pane>
                <span
                    slot="label"
                    class="tab-label"
                >
                    <el-dropdown @command="handleCommand" style="margin-top: -3px">
                        <span class="el-dropdown-link">
                            批量操作<i class="el-icon-arrow-down el-icon--right"></i>
                        </span>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item command="export">导出数据</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                    <div style="height: 5px; background: blue; width: 60px; margin-top:-8px; ; border-radius: 6px"></div>
                </span>
                <bk-table
                    height="350"
                    :data="history"
                    :size="medium"
                    :pagination="pagination"
                    @select="selectRow"
                    @select-all="selectAll"
                    @page-change="handlePageChange"
                    @page-limit-change="handlePageLimitChange"
                    :header-cell-style="{ background: '#fff' }"
                >
                    <bk-table-column
                        type="selection"
                        width="60"
                    ></bk-table-column>
                    <bk-table-column
                        label="物品名称"
                        width="80"
                    >
                        <template slot-scope="props">
                            <bk-input
                                v-model="props.row.good_name"
                                v-if="editId === props.row.id"
                            ></bk-input>
                            <div v-else>
                                {{props.row.good_name}}
                            </div>
                        </template>
                    </bk-table-column>
                    <bk-table-column
                        label="物品编码"
                        width="100"
                    >
                        <template slot-scope="props">
                            <bk-input
                                v-model="props.row.good_code"
                                v-if="editId === props.row.id"
                            ></bk-input>
                            <div v-else>
                                {{props.row.good_code}}
                            </div>
                        </template>
                    </bk-table-column>
                    <bk-table-column
                        label="申请时间"
                        prop="create_time"
                        width="180"
                    >
                        <template slot-scope="props">
                            <bk-tag ext-cls="custom-tag">{{props.row.create_time}}</bk-tag>
                        </template>
                    </bk-table-column>
                    <bk-table-column
                        label="数量"
                        width="100"
                    >
                        <template slot-scope="props">
                            <bk-input
                                v-model="props.row.num"
                                v-if="editId === props.row.id"
                                type="number"
                                :precision="0"
                                :min="1"
                            ></bk-input>
                            <div v-else>
                                {{props.row.num}}
                            </div>
                        </template>
                    </bk-table-column>
                    <bk-table-column label="申请原因">
                        <template slot-scope="props">
                            <bk-input
                                v-model="props.row.reason"
                                v-if="editId === props.row.id"
                            ></bk-input>
                            <div v-else>
                                {{props.row.reason}}
                            </div>
                        </template>
                    </bk-table-column>
                    <bk-table-column
                        label="状态"
                        width="150"
                    >
                        <template slot-scope="props">
                            <bk-tag :theme="getStatusTheme(props.row.status)">{{ props.row.status }}</bk-tag>
                        </template>
                    </bk-table-column>
                    <bk-table-column
                        label="审核人"
                        prop="reviewer"
                        width="120"
                    ></bk-table-column>
                    <bk-table-column
                        label="审核日期"
                        width="180"
                    >
                        <template slot-scope="props">
                            <bk-tag ext-cls="custom-tag">{{moment(props.row.review_time).format('YYYY-MM-DD HH:mm:ss')}}</bk-tag>
                        </template>
                    </bk-table-column>
                    <bk-table-column
                        label="备注"
                        prop="reason"
                    ></bk-table-column>
                    <bk-table-column
                        label="操作"
                        width="150"
                    >
                        <template slot-scope="props">
                            <bk-button
                                class="mr10"
                                theme="primary"
                                text
                                @click="clickEdit(props.row)"
                                :disabled="props.row.status !== '导员审核中'"
                            >编辑</bk-button>
                            <bk-button
                                class="mr10"
                                theme="primary"
                                text
                                @click="confirmEdit(props.row)"
                                v-if="editId === props.row.id"
                            >保存</bk-button>
                            <bk-popconfirm
                                content="确定删除记录？"
                                width="280"
                                @confirm="confirmDelete(props.row)"
                                trigger="click"
                            >
                                <bk-button
                                    :disabled="props.row.status === '管理员审核中'"
                                    class="mr10"
                                    theme="primary"
                                    text
                                >删除</bk-button>
                            </bk-popconfirm>
                        </template>
                    </bk-table-column>
                </bk-table>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    import {
        deriveExcelUrl, getGoodApplyListUrl, editApplyUrl, deleteApplyUrl
    } from '@/pattern'
    export default {
        data () {
            return {
                selected: {
                    selectedRows: [] // 存放被选中行数
                },
                getParams: {
                    good_name: '',
                    good_code: '',
                    reason: '',
                    start_time: '',
                    end_time: '',
                    status: '',
                    size: 10,
                    page: 1
                },
                history: [],
                pagination: { // 分页器数据
                    current: 1,
                    count: 10,
                    limit: 10
                },
                isDropdownShow: false,
                editId: null
            }
        },
        created () {
            this.getGoodApplyList()
        },
        methods: {
            getGoodApplyList () {
                this.editId = null
                this.$http.get(getGoodApplyListUrl, {
                    params: {
                        start_time: this.getParams.start_time,
                        end_time: this.getParams.end_time,
                        good_code: this.getParams.good_code,
                        good_name: this.getParams.good_name,
                        reason: this.getParams.reason,
                        status: this.getParams.status,
                        page: this.getParams.page,
                        size: this.getParams.size
                    }
                }).then(res => {
                    this.history = res.data.apply_list
                    this.pagination.count = res.data.total_num
                })
            },
            exportData () {
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.$http.post(deriveExcelUrl, { model: 3, dataList: this.selected }).then(res => {
                    if (res && res.result === true) {
                        const link = document.createElement('a') // 生成a元素，用以实现下载功能
                        link.href = res.data.file_url
                        document.body.appendChild(link)
                        link.click()
                        document.body.removeChild(link)
                        this.getGoodApplyList()
                        this.selected.selectedRows = []
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                })
            },
            search (formData) {
                this.getParams.start_time = formData.startDate ? this.moment(formData.startDate).format('YYYY-MM-DD') : ''
                this.getParams.end_time = formData.endDate ? this.moment(formData.endDate).format('YYYY-MM-DD') : ''
                this.getParams.status = formData.status
                if (formData.status === 999 || formData.status === '999') {
                    this.getParams.status = ''
                }
                this.getParams.good_name = formData.good_name
                this.getParams.good_code = formData.good_code
                this.getParams.reason = formData.apply_reason

                this.pagination.current = 1
                this.getParams.page = this.pagination.current
                this.getGoodApplyList()
            },
            selectRow (selection, row) { // 选择单行时触发函数
                const idx = this.selected.selectedRows.indexOf(row.id)
                if (idx !== -1) {
                    this.selected.selectedRows.splice(idx, 1)
                } else {
                    this.selected.selectedRows.push(row.id)
                }
            },
            selectAll () { // 全选时触发函数
                let ifFullPage = true
                for (let index = 0; index < this.history.length; index++) {
                    const ifIdx = this.selected.selectedRows.indexOf(this.history[index].id)
                    if (ifIdx === -1) {
                        ifFullPage = false
                    }
                    if (!ifFullPage) {
                        break
                    }
                }
                if (this.selected.selectedRows.length !== 0 && !ifFullPage) {
                    for (let index = 0; index < this.history.length; index++) {
                        if (this.selected.selectedRows.indexOf(this.history[index].id) === -1) {
                            this.selected.selectedRows.push(this.history[index].id)
                        }
                    }
                } else if (this.selected.selectedRows.length !== 0 && ifFullPage) {
                    for (let index = 0; index < this.history.length; index++) {
                        const delIdx = this.selected.selectedRows.indexOf(this.history[index].id)
                        this.selected.selectedRows.splice(delIdx, 1)
                    }
                } else if (this.selected.selectedRows.length === 0) {
                    for (let index = 0; index < this.history.length; index++) {
                        this.selected.selectedRows.push(this.history[index].id)
                    }
                }
            },
            clickEdit (row) {
                this.editId = row.id
            },
            confirmEdit (row) {
                this.$http.patch(editApplyUrl, {
                    id: row.id,
                    good_code: row.good_code,
                    good_name: row.good_name,
                    num: row.num,
                    reason: row.reason
                }).then(res => {
                    if (res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                        this.getGoodApplyList()
                    }
                })
            },
            confirmDelete (row) {
                this.$http.delete(`/apply/${row.id}/${deleteApplyUrl}`).then(res => {
                    if (res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                        this.getGoodApplyList()
                    }
                })
            },
            handlePageLimitChange () { // 修改每页多少条数据触发函数
                this.pagination.limit = arguments[0]
                this.getParams.size = this.pagination.limit
                this.pagination.current = 1
                this.getParams.page = this.pagination.current
                this.selected.selectedRows = []
                this.getGoodApplyList()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.getParams.page = this.pagination.current
                this.getGoodApplyList()
            },
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            },
            getStatusTheme (status) {
                let theme = ''
                switch (status) {
                    case '申请终止':
                        theme = 'danger'
                        break
                    case '导员审核中':
                        theme = 'info'
                        break
                    case '管理员审核中':
                        theme = 'warning'
                        break
                    case '审核完成':
                        theme = 'success'
                        break
                    default:
                        theme = ''
                        break
                }
                return theme
            },
            handleCommand (command) {
                if (command === 'export') {
                    this.exportData()
                }
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .table-content {
        .tab-label {
            display: flex;
            flex-direction: column;
            place-content: center;
            place-items: center;
            .el-dropdown-link {
            }
        }
    }
    .custom-tag {
        color: #2dcb56;
    }
    /deep/.bk-table-enable-row-transition .bk-table-body td {
        border: none !important;
    }
    /deep/.bk-table {
        border: none !important;
        &:before {
            height: 0px !important;
        }
    }
    /deep/.bk-table-outer-border:after {
        width: 0px !important;
    }
    /deep/.bk-table-pagination-wrapper {
        border: none !important;
    }
    /deep/.el-tabs__nav {
        float: right;
    }
    /deep/.el-tabs__item {
        width: 120px;
        height: 50px;
        display: flex;
        flex-direction: column;
        place-content: center;
        place-items: center;
        border: #409eff solid 2px;
        border-radius: 8px;
    }
    /deep/.el-tabs__active-bar {
        display: none;
    }
    /deep/.el-tabs__nav-wrap::after {
        background-color: #409eff;
    }
</style>
