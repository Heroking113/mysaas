<template>
    <div class="magic-footer">
        <div class="magic-copyright">
            <p>
                <a href="wxwork://message/?username=BK助手" id="contact-us" class="link magic-contact">
                    <img src="@doc/images/wx-work.png" />
                    <span>蓝鲸助手</span>
                </a>
                Copyright © 2012-<span id="cur_year">{{year}}</span> Tencent BlueKing. All Rights Reserved. 蓝鲸智云 版权所有
            </p>
        </div>
        <div class="magic-button">
            <a href="javascript:void(0);" class="magic-top" v-show="showBackTop" @click="backTop">
                <img src="@doc/images/back-top.png" alt="返回顶部" />
            </a>
            <a href="http://ce.oa.com/products/view/2247?&tab_id=all_issues_btn#create-feedback" target="_blank" class="magic-feedback">
                <img src="@doc/images/feedback.png" alt="反馈" />
            </a>
        </div>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                year: new Date().getFullYear(),
                showBackTop: false
            }
        },
        mounted () {
            window.addEventListener('scroll', this.toggleBackTop)
        },
        destroyed () {
            window.removeEventListener('scroll', this.toggleBackTop)
        },
        methods: {
            /**
             * 获取页面滚动高度，判断是否出现返回顶部
             */
            toggleBackTop () {
                let scrollTop = 0
                let bodyScrollTop = 0
                let documentScrollTop = 0

                if (document.body) {
                    bodyScrollTop = document.body.scrollTop
                }

                if (document.documentElement) {
                    documentScrollTop = document.documentElement.scrollTop
                }

                scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop
                this.showBackTop = scrollTop > 0
            },

            /**
             * 返回到页面顶部
             */
            backTop () {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                })
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import '@doc/css/footer.css';
</style>
