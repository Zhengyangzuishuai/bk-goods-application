<template>
    <div class="userCenter-wrapper">
        <div
            class="Info"
            style="width: 100%;"
        >
            <bk-form
                :label-width="100"
                :model="userInfo"
                :rules="rules"
                ref="userInfo"
                class="InfoForm"
            >
                <bk-container
                    :col="12"
                    :gutter="8"
                >
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="9">
                            <bk-form-item
                                :label-width="80"
                                label="用户名"
                                :required="true"
                                :property="'name'"
                                :error-display-type="'normal'"
                            >
                                <bk-input
                                    class="userCenterInput"
                                    v-model="userInfo.username"
                                    placeholder="请输入新的用户名"
                                    :disabled="true"
                                ></bk-input>
                            </bk-form-item>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="10">
                            <bk-form-item
                                :label-width="80"
                                label="所在地区"
                                :error-display-type="'normal'"
                                :required="true"
                                :property="'position'"
                            >
                                <bk-select
                                    :disabled="editable"
                                    v-model="userInfo.position"
                                    style="width: 80%"
                                    ext-cls="select-custom"
                                    ext-popover-cls="select-popover-custom"
                                    searchable
                                >
                                    <bk-option
                                        v-for="option in locationList"
                                        :key="option.id"
                                        :id="option.name"
                                        :name="option.name"
                                    >
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 30px;">
                        <bk-col :span="9">
                            <bk-form-item
                                :label-width="80"
                                label="手机号码"
                                :property="'phone'"
                                :error-display-type="'normal'"
                            >
                                <bk-input
                                    class="userCenterInput"
                                    v-model="userInfo.phone"
                                    placeholder="号码为空"
                                    :disabled="editable"
                                ></bk-input>
                            </bk-form-item>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="6">
                            <bk-button
                                style="margin-left: 60%"
                                :theme="'primary'"
                                :title="'修改信息'"
                                class="mr10"
                                @click="editInfo"
                                v-if="editable"
                            >
                                修改信息
                            </bk-button>
                            <bk-button
                                style="margin-left: 10%"
                                :theme="'warning'"
                                :title="'取消修改'"
                                class="mr10"
                                @click="cancelEdit"
                                v-if="!editable"
                            >
                                取消修改
                            </bk-button>
                        </bk-col>
                        <bk-col :span="6">
                            <bk-button
                                style="margin-left: 10%"
                                :theme="'success'"
                                :title="'确定修改'"
                                @click="confirmEdit"
                                v-if="!editable"
                            >
                                确定修改
                            </bk-button>
                            <bk-dialog
                                v-model="submitDialogVisible"
                                width="400"
                                :render-directive="'if'"
                                :mask-close="false"
                                :header-position="left"
                                @confirm="submitEdit"
                                :esc-close="false"
                            >
                                确定修改?
                            </bk-dialog>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </bk-form>
        </div>
    </div>
</template>

<script>
    import { getPositionsUrl, editUserInfoUrl } from '@/pattern'
    import { mapState } from 'vuex'

    export default {
        data () {
            return {
                editable: true,
                locationList: '',
                submitDialogVisible: false,
                rules: {
                    name: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            max: 30,
                            message: '不能多于30个字符',
                            trigger: 'blur'
                        }
                    ],
                    phone: [
                        {
                            max: 11,
                            message: '不能多于11个字符',
                            trigger: 'blur'
                        },
                        {
                            validator: this.checkPhone,
                            message: '号码格式错误',
                            trigger: 'blur'
                        }
                    ],
                    position: [
                        {
                            required: true,
                            message: '请选择地区',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo,
                globalLoading: state => state.patient.loading
            })
        },
        methods: {
            loadData () {
                this.getPosition()
            },
            getPosition () { // 获得所有地点
                this.$http.get(getPositionsUrl).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.locationList = res.data
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            editInfo () {
                this.editable = false
            },
            cancelEdit () {
                this.editable = true
                this.$refs.userInfo.clearError()
            },
            confirmEdit () {
                this.$refs.userInfo.validate().then(validator => {
                    this.submitDialogVisible = true
                })
            },
            submitEdit () {
                this.$http.post(editUserInfoUrl, { phone: this.userInfo.phone, position: this.userInfo.position }).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.handleError({ theme: 'success' }, res.message)
                            this.editable = true
                            this.$refs.userInfo.clearError()
                            this.$store.dispatch('user/userInfo')
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .userCenter-wrapper {
        .Info {
            .userCenterInput {
                width: 94%;
            }
            .InfoForm {
                /deep/.mt20 {
                    text-align: center;
                }
            }
        }
    }
</style>
