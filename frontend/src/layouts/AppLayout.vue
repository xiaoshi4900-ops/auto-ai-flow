<template>
  <el-container class="app-layout" data-testid="workspace-shell">
    <el-aside width="248px" class="sidebar" data-testid="workspace-sidebar">
      <div class="logo">
        <p class="logo-kicker">AI Agent Platform</p>
        <h2>AutoAiFlow</h2>
        <span class="logo-badge">MVP / Observability UI</span>
      </div>
      <el-menu :default-active="route.path" router class="sidebar-menu" data-testid="workspace-nav">
        <el-menu-item index="/projects">
          <el-icon><Folder /></el-icon>
          <span>项目空间</span>
        </el-menu-item>
        <el-menu-item index="/agents">
          <el-icon><User /></el-icon>
          <span>Agent 管理</span>
        </el-menu-item>
        <el-menu-item index="/models">
          <el-icon><Setting /></el-icon>
          <span>模型配置</span>
        </el-menu-item>
        <el-menu-item index="/workflows">
          <el-icon><Share /></el-icon>
          <span>Workflow</span>
        </el-menu-item>
        <el-menu-item index="/runs">
          <el-icon><VideoPlay /></el-icon>
          <span>运行记录</span>
        </el-menu-item>
        <el-menu-item :index="ROUTES.UI_REFERENCE">
          <el-icon><Monitor /></el-icon>
          <span>UI 参考页</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="app-header" data-testid="workspace-header">
        <div class="header-left">
          <div class="project-pill" data-testid="workspace-pill">
            <span class="project-pill__dot"></span>
            内容智能体平台 / 一期
          </div>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info" data-testid="workspace-user-menu">
              {{ authStore.user?.username || 'Operator' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="authStore.logout()">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="app-main" data-testid="workspace-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Folder, User, Setting, Share, VideoPlay, ArrowDown, Monitor } from '@element-plus/icons-vue'
import { ROUTES } from '@/constants/routes'

const route = useRoute()
const authStore = useAuthStore()
</script>

<style scoped>
.app-layout {
  height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(60, 185, 255, 0.12), transparent 30%),
    linear-gradient(180deg, #07111a 0%, #09131d 100%);
}
.sidebar {
  background: rgba(7, 14, 24, 0.96);
  color: var(--text-primary);
  border-right: 1px solid rgba(160, 190, 210, 0.12);
  box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.02);
}
.logo {
  padding: 22px 20px 18px;
}
.logo-kicker {
  margin: 0 0 8px;
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.logo h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 26px;
}
.logo-badge {
  display: inline-flex;
  margin-top: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 12px;
}
.sidebar-menu {
  border-right: none;
  --el-menu-bg-color: transparent;
  --el-menu-text-color: var(--text-secondary);
  --el-menu-hover-bg-color: rgba(255, 255, 255, 0.05);
  --el-menu-active-color: var(--text-primary);
  --el-menu-item-height: 48px;
  background: transparent;
  padding: 8px 12px;
}
:deep(.sidebar-menu .el-menu-item) {
  margin-bottom: 6px;
  border-radius: 14px;
}
:deep(.sidebar-menu .el-menu-item.is-active) {
  background: linear-gradient(135deg, rgba(86, 240, 192, 0.12), rgba(60, 185, 255, 0.14));
  border: 1px solid rgba(86, 240, 192, 0.2);
}
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid rgba(160, 190, 210, 0.12);
  background: rgba(7, 14, 24, 0.54);
  backdrop-filter: blur(16px);
}
.header-left,
.header-right {
  display: flex;
  align-items: center;
}
.project-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  height: 38px;
  padding: 0 14px;
  border-radius: 999px;
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.project-pill__dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, #56f0c0, #3cb9ff);
  box-shadow: 0 0 12px rgba(86, 240, 192, 0.75);
}
.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-primary);
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.app-main {
  background: transparent;
  min-height: 0;
  padding: 0;
}
</style>
