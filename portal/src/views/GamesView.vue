<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">الألعاب التعليمية</h1>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card text-center py-10">
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button @click="fetchGames" class="btn-primary">إعادة المحاولة</button>
    </div>

    <template v-else>
      <!-- Games Grid -->
      <div v-if="games.length === 0" class="card text-center py-16 mb-8">
        <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="text-gray-500 text-lg">لا توجد ألعاب متاحة حالياً</p>
      </div>

      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5 mb-10">
        <div
          v-for="game in games"
          :key="game.id"
          @click="openGame(game)"
          class="card p-0 overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group"
        >
          <div class="aspect-square bg-gray-100 relative overflow-hidden">
            <img
              v-if="game.thumbnail_url"
              :src="game.thumbnail_url"
              :alt="game.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
            <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-100 to-purple-200">
              <svg class="w-12 h-12 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div v-if="game.age_range" class="absolute top-2 right-2 bg-white/90 text-xs font-medium px-2 py-1 rounded-full">
              {{ game.age_range }}
            </div>
          </div>
          <div class="p-3">
            <h3 class="font-bold text-sm truncate">{{ game.title }}</h3>
            <p v-if="game.category?.name" class="text-xs text-gray-500 mt-1">{{ game.category.name }}</p>
          </div>
        </div>
      </div>

      <!-- AI Voice Practice Section -->
      <div class="card">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-lg font-bold">تدريب النطق بالذكاء الاصطناعي</h2>
            <p class="text-sm text-gray-500">تدرب على نطق الكلمات واحصل على تقييم فوري</p>
          </div>
        </div>

        <!-- Practice Word Display -->
        <div v-if="practiceWordsLoading" class="flex justify-center py-6">
          <div class="animate-spin rounded-full h-8 w-8 border-4 border-green-500 border-t-transparent"></div>
        </div>

        <template v-else>
          <div v-if="practiceWords.length > 0" class="mb-6">
            <!-- Current Word -->
            <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 text-center mb-4">
              <p class="text-sm text-gray-500 mb-2">انطق هذه الكلمة:</p>
              <p class="text-4xl font-bold text-green-700 mb-2">{{ currentWord.arabic }}</p>
              <p v-if="currentWord.transliteration" class="text-sm text-gray-400">{{ currentWord.transliteration }}</p>
            </div>

            <!-- Word Navigation -->
            <div class="flex items-center justify-center gap-4 mb-6">
              <button
                @click="prevWord"
                :disabled="currentWordIndex === 0"
                class="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </button>
              <span class="text-sm text-gray-500">{{ currentWordIndex + 1 }} / {{ practiceWords.length }}</span>
              <button
                @click="nextWord"
                :disabled="currentWordIndex >= practiceWords.length - 1"
                class="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                </svg>
              </button>
            </div>

            <!-- Record Button -->
            <div class="flex flex-col items-center gap-4">
              <button
                @click="toggleRecording"
                class="w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 shadow-lg"
                :class="isRecording ? 'bg-red-500 animate-pulse scale-110' : 'bg-green-500 hover:bg-green-600 hover:scale-105'"
              >
                <svg v-if="!isRecording" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
                </svg>
                <svg v-else class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"/>
                </svg>
              </button>
              <p class="text-sm text-gray-500">
                {{ isRecording ? 'جارٍ التسجيل... اضغط للإيقاف' : 'اضغط للتسجيل' }}
              </p>
            </div>

            <!-- Speech Not Supported Warning -->
            <div v-if="speechNotSupported" class="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-center">
              <p class="text-sm text-yellow-800">متصفحك لا يدعم التعرف على الصوت. يرجى استخدام متصفح Chrome.</p>
            </div>

            <!-- Evaluating -->
            <div v-if="evaluating" class="mt-6 flex justify-center">
              <div class="animate-spin rounded-full h-8 w-8 border-4 border-green-500 border-t-transparent"></div>
            </div>

            <!-- Evaluation Result -->
            <div v-if="evaluationResult && !evaluating" class="mt-6">
              <div class="bg-white border-2 rounded-2xl p-6 text-center" :class="resultBorderClass">
                <div class="mb-3">
                  <span class="text-5xl font-bold" :class="resultTextClass">{{ evaluationResult.score }}</span>
                  <span class="text-lg text-gray-400">/100</span>
                </div>
                <p class="text-lg font-bold mb-1" :class="resultTextClass">{{ feedbackLabel }}</p>
                <p v-if="evaluationResult.feedback" class="text-sm text-gray-500">{{ evaluationResult.feedback }}</p>
                <p v-if="recognizedText" class="text-sm text-gray-400 mt-2">
                  ما تم التقاطه: <span class="font-medium">{{ recognizedText }}</span>
                </p>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-6 text-gray-500">
            <p>لا توجد كلمات تدريب متاحة حالياً</p>
            <button @click="fetchPracticeWords" class="btn-secondary mt-3">إعادة المحاولة</button>
          </div>
        </template>
      </div>
    </template>

    <!-- Game Detail Modal -->
    <div v-if="selectedGame" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50" @click="selectedGame = null"></div>
      <div class="relative bg-white rounded-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <button @click="selectedGame = null" class="absolute top-4 left-4 p-2 rounded-lg hover:bg-gray-100 z-10">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
        <div class="aspect-video bg-gray-100 rounded-t-2xl overflow-hidden">
          <img v-if="selectedGame.thumbnail_url" :src="selectedGame.thumbnail_url" :alt="selectedGame.title" class="w-full h-full object-cover"/>
        </div>
        <div class="p-6">
          <h2 class="text-xl font-bold mb-2">{{ selectedGame.title }}</h2>
          <p v-if="selectedGame.description" class="text-gray-600 text-sm leading-relaxed mb-4">{{ selectedGame.description }}</p>
          <div class="flex gap-3">
            <button v-if="selectedGame.content_url" @click="launchGame(selectedGame)" class="btn-primary flex-1">ابدأ اللعب</button>
            <button @click="selectedGame = null" class="btn-secondary flex-1">إغلاق</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { contentApi, voiceApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const games = ref([])
const selectedGame = ref(null)
const loading = ref(false)
const error = ref(null)

// Voice practice state
const practiceWords = ref([])
const practiceWordsLoading = ref(false)
const currentWordIndex = ref(0)
const isRecording = ref(false)
const evaluating = ref(false)
const recognizedText = ref('')
const evaluationResult = ref(null)
const speechNotSupported = ref(false)

let recognition = null

const currentWord = computed(() => practiceWords.value[currentWordIndex.value] || { arabic: '', transliteration: '' })

const feedbackLabel = computed(() => {
  if (!evaluationResult.value) return ''
  const score = evaluationResult.value.score
  if (score >= 90) return 'ممتاز'
  if (score >= 75) return 'جيد جداً'
  if (score >= 60) return 'جيد'
  return 'يحتاج تدريب'
})

const resultBorderClass = computed(() => {
  if (!evaluationResult.value) return 'border-gray-200'
  const score = evaluationResult.value.score
  if (score >= 90) return 'border-green-400'
  if (score >= 75) return 'border-blue-400'
  if (score >= 60) return 'border-yellow-400'
  return 'border-red-400'
})

const resultTextClass = computed(() => {
  if (!evaluationResult.value) return 'text-gray-600'
  const score = evaluationResult.value.score
  if (score >= 90) return 'text-green-600'
  if (score >= 75) return 'text-blue-600'
  if (score >= 60) return 'text-yellow-600'
  return 'text-red-600'
})

function prevWord() {
  if (currentWordIndex.value > 0) {
    currentWordIndex.value--
    evaluationResult.value = null
    recognizedText.value = ''
  }
}

function nextWord() {
  if (currentWordIndex.value < practiceWords.value.length - 1) {
    currentWordIndex.value++
    evaluationResult.value = null
    recognizedText.value = ''
  }
}

function openGame(game) {
  selectedGame.value = game
}

function launchGame(game) {
  if (game.content_url) {
    window.open(game.content_url, '_blank')
  }
}

function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SpeechRecognition) {
    speechNotSupported.value = true
    return
  }

  recognition = new SpeechRecognition()
  recognition.lang = 'ar-SA'
  recognition.interimResults = false
  recognition.maxAlternatives = 1

  recognition.onresult = async (event) => {
    const transcript = event.results[0][0].transcript
    recognizedText.value = transcript
    isRecording.value = false
    await evaluatePronunciation(transcript)
  }

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error)
    isRecording.value = false
  }

  recognition.onend = () => {
    isRecording.value = false
  }
}

function toggleRecording() {
  if (speechNotSupported.value || !recognition) return

  if (isRecording.value) {
    recognition.stop()
    isRecording.value = false
  } else {
    evaluationResult.value = null
    recognizedText.value = ''
    isRecording.value = true
    recognition.start()
  }
}

async function evaluatePronunciation(transcript) {
  evaluating.value = true
  try {
    const { data } = await voiceApi.evaluate({
      word_id: currentWord.value.id,
      expected: currentWord.value.arabic,
      recognized: transcript,
    })
    evaluationResult.value = data
  } catch (err) {
    console.error('Failed to evaluate pronunciation:', err)
    evaluationResult.value = { score: 0, feedback: 'حدث خطأ أثناء التقييم. يرجى المحاولة مرة أخرى.' }
  } finally {
    evaluating.value = false
  }
}

async function fetchGames() {
  loading.value = true
  error.value = null
  try {
    const { data } = await contentApi.getItems({ type: 'game' })
    games.value = data?.items || data || []
  } catch (err) {
    error.value = 'حدث خطأ أثناء تحميل الألعاب. يرجى المحاولة مرة أخرى.'
    console.error('Failed to fetch games:', err)
  } finally {
    loading.value = false
  }
}

async function fetchPracticeWords() {
  practiceWordsLoading.value = true
  try {
    const { data } = await voiceApi.getWords()
    practiceWords.value = data?.words || data || []
    currentWordIndex.value = 0
  } catch (err) {
    console.error('Failed to fetch practice words:', err)
  } finally {
    practiceWordsLoading.value = false
  }
}

onMounted(() => {
  fetchGames()
  fetchPracticeWords()
  initSpeechRecognition()
})

onUnmounted(() => {
  if (recognition && isRecording.value) {
    recognition.stop()
  }
})
</script>
