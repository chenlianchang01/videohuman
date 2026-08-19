<template>
  <div class="login-wrap">
    <el-card class="login-card">
      <h2>videohuman 工作台</h2>
      <p class="tip">该实例已启用访问令牌,请输入 token 继续</p>
      <el-input v-model="token" placeholder="访问 token" show-password style="width: 320px"
        @keyup.enter="submit" />
      <div style="margin-top: 16px">
        <el-button type="primary" :loading="checking" @click="submit">进入</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getSettings, setToken } from '../api.js'

const route = useRoute()
const router = useRouter()
const token = ref('')
const checking = ref(false)

async function submit() {
  if (!token.value.trim()) return ElMessage.warning('请输入 token')
  checking.value = true
  try {
    setToken(token.value.trim())
    await getSettings() // 验证 token 有效性(失败会被拦截器清掉并 401)
    router.replace(typeof route.query.back === 'string' ? route.query.back : '/')
  } catch {
    ElMessage.error('token 错误')
  } finally {
    checking.value = false
  }
}
</script>

<style scoped>
.login-wrap { display: flex; justify-content: center; padding-top: 120px; }
.login-card { text-align: center; padding: 16px 32px; }
.tip { color: #909399; font-size: 13px; }
</style>
