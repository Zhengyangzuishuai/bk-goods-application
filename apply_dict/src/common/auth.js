/**
 * @file auth
 * @author wheel-w
 */

import store from '@/store'

const ANONYMOUS_USER = {
    id: null,
    isAuthenticated: false,
    username: 'anonymous'
}

let currentUser = {
    id: '',
    username: ''
}

export default {
    /**
     * 未登录状态码
     */
    HTTP_STATUS_UNAUTHORIZED: 401,

    /**
     * 获取当前用户
     *
     * @return {Object} 当前用户信息
     */
    getCurrentUser () {
        return currentUser
    },

    /**
     * 请求当前用户信息
     *
     * @return {Promise} promise 对象
     */
    requestCurrentUser () {
        let promise = null
        if (currentUser.isAuthenticated) {
            promise = new Promise((resolve, reject) => {
                resolve(currentUser)
            })
        } else {
            if (!store.state.user.userInfo || !Object.keys(store.state.user.userInfo).length) {
                // store action userInfo 里，如果请求成功会更新 state.user
                const req = store.dispatch('user/userInfo')
                promise = new Promise((resolve, reject) => {
                    req.then(resp => {
                        // 存储当前用户信息(全局)
                        currentUser = store.state.user.userInfo
                        currentUser.isAuthenticated = true
                        resolve(currentUser)
                    }, err => {
                        if (err.response.status === this.HTTP_STATUS_UNAUTHORIZED || err.crossDomain) {
                            resolve({ ...ANONYMOUS_USER })
                        } else {
                            reject(err)
                        }
                    })
                })
            }
        }

        return promise
    }
}
