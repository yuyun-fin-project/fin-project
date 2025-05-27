<template>
  <div class="bg-white rounded-xl shadow-lg p-6 h-full flex flex-col">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-900">주변 은행 찾기</h2>
    </div>
    <div class="flex-1 flex flex-col">
      <div class="search-container mb-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- 도/시 선택 -->
          <div class="relative">
            <select 
              v-model="selectedCity"
              @change="onCityChange"
              class="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none"
            >
              <option value="">도/시 선택</option>
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
          
          <!-- 시/군/구 선택 -->
          <div class="relative">
            <select 
              v-model="selectedDistrict"
              @change="onDistrictChange"
              :disabled="!selectedCity"
              class="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none disabled:bg-gray-100 disabled:text-gray-500"
            >
              <option value="">시/군/구 선택</option>
              <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>

          <!-- 은행 선택 -->
          <div class="relative">
            <select 
              v-model="selectedBank"
              @change="searchPlaces"
              :disabled="!selectedDistrict"
              class="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none disabled:bg-gray-100 disabled:text-gray-500"
            >
              <option value="">은행 선택</option>
              <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
      </div>
      <div id="kakao-map" class="map-container flex-1"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const KAKAO_MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY
const selectedCity = ref('')
const selectedDistrict = ref('')
const selectedBank = ref('')
const map = ref(null)
const markers = ref([])
const activeInfoWindow = ref(null)
let isScriptLoaded = false

// 도/시 목록
const cities = [
  '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
  '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도',
  '충청북도', '충청남도', '전라북도', '전라남도', '경상북도',
  '경상남도', '제주특별자치도'
]

// 은행 목록
const banks = [
  '국민은행', '신한은행', '우리은행', '하나은행', 'SC제일은행',
  'NH농협은행', 'IBK기업은행', '수협은행', '부산은행', '대구은행',
  '경남은행', '광주은행', '전북은행', '제주은행', 'KDB산업은행',
  '한국수출입은행', '한국씨티은행', '케이뱅크', '카카오뱅크', '토스뱅크'
]

// 시/군/구 목록 (선택된 도시에 따라 동적으로 변경)
const districts = ref([])

// 도시별 시/군/구 데이터
const districtsByCity = {
  '서울특별시': ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', 
                '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', 
                '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'],
  '부산광역시': ['강서구', '금정구', '남구', '동구', '동래구', '부산진구', '북구', '사상구', 
                '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구', '기장군'],
  '대구광역시': ['남구', '달서구', '동구', '북구', '서구', '수성구', '중구', '달성군'],
  '인천광역시': ['계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '중구', '강화군', '옹진군'],
  '광주광역시': ['광산구', '남구', '동구', '북구', '서구'],
  '대전광역시': ['대덕구', '동구', '서구', '유성구', '중구'],
  '울산광역시': ['남구', '동구', '북구', '중구', '울주군'],
  '세종특별자치시': ['세종시'],
  '경기도': ['수원시', '성남시', '의정부시', '안양시', '부천시', '광명시', '평택시', '동두천시', 
            '안산시', '고양시', '과천시', '구리시', '남양주시', '오산시', '시흥시', '군포시', 
            '의왕시', '하남시', '용인시', '파주시', '이천시', '안성시', '김포시', '화성시', 
            '광주시', '양주시', '포천시', '여주시', '연천군', '가평군', '양평군'],
  '강원도': ['춘천시', '원주시', '강릉시', '동해시', '태백시', '속초시', '삼척시',
            '홍천군', '횡성군', '영월군', '평창군', '정선군', '철원군', '화천군',
            '양구군', '인제군', '고성군', '양양군'],
  '충청북도': ['청주시', '충주시', '제천시', '보은군', '옥천군', '영동군', '증평군',
              '진천군', '괴산군', '음성군', '단양군'],
  '충청남도': ['천안시', '공주시', '보령시', '아산시', '서산시', '논산시', '계룡시',
              '당진시', '금산군', '부여군', '서천군', '청양군', '홍성군', '예산군',
              '태안군'],
  '전라북도': ['전주시', '군산시', '익산시', '정읍시', '남원시', '김제시', '완주군',
              '진안군', '무주군', '장수군', '임실군', '순창군', '고창군', '부안군'],
  '전라남도': ['목포시', '여수시', '순천시', '나주시', '광양시', '담양군', '곡성군',
              '구례군', '고흥군', '보성군', '화순군', '장흥군', '강진군', '해남군',
              '영암군', '무안군', '함평군', '영광군', '장성군', '완도군', '진도군',
              '신안군'],
  '경상북도': ['포항시', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시',
              '상주시', '문경시', '경산시', '군위군', '의성군', '청송군', '영양군',
              '영덕군', '청도군', '고령군', '성주군', '칠곡군', '예천군', '봉화군',
              '울진군', '울릉군'],
  '경상남도': ['창원시', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시',
              '양산시', '의령군', '함안군', '창녕군', '고성군', '남해군', '하동군',
              '산청군', '함양군', '거창군', '합천군'],
  '제주특별자치도': ['제주시', '서귀포시']
}

const loadKakaoMapScript = () => {
  return new Promise((resolve, reject) => {
    try {
      if (window.kakao && window.kakao.maps) {
        isScriptLoaded = true
        resolve(window.kakao.maps)
        return
      }

      const script = document.createElement('script')
      script.type = 'text/javascript'
      // services 라이브러리만 사용
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_API_KEY}&libraries=services&autoload=false`

      script.onload = () => {
        window.kakao.maps.load(() => {
          isScriptLoaded = true
          resolve(window.kakao.maps)
        })
      }

      script.onerror = (error) => {
        reject(error)
      }

      document.head.appendChild(script)
    } catch (error) {
      reject(error)
    }
  })
}

const initMap = async () => {
  try {
    const maps = await loadKakaoMapScript()
    
    const container = document.getElementById('kakao-map')
    if (!container) {
      throw new Error('지도를 표시할 DOM 엘리먼트를 찾을 수 없습니다.')
    }

    const options = {
      center: new maps.LatLng(37.5665, 126.9780),
      level: 3
    }

    const mapInstance = new maps.Map(container, options)
    map.value = mapInstance
  } catch (error) {
    console.error('지도 초기화 중 오류 발생:', error)
  }
}

const closeActiveInfoWindow = () => {
  if (activeInfoWindow.value) {
    activeInfoWindow.value.close()
    activeInfoWindow.value = null
  }
}

const onCityChange = () => {
  selectedDistrict.value = ''
  selectedBank.value = ''
  districts.value = districtsByCity[selectedCity.value] || []
}

const onDistrictChange = () => {
  selectedBank.value = ''
  if (selectedDistrict.value) {
    searchPlaces()
  }
}

const searchPlaces = () => {
  if (!selectedCity.value || !selectedDistrict.value || !map.value || !isScriptLoaded) return

  const searchQuery = `${selectedCity.value} ${selectedDistrict.value} ${selectedBank.value || ''} 은행`
  const ps = new kakao.maps.services.Places()
  
  ps.keywordSearch(searchQuery, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      // 기존 마커와 인포윈도우 제거
      closeActiveInfoWindow()
      markers.value.forEach(marker => marker.setMap(null))
      markers.value = []

      const bounds = new kakao.maps.LatLngBounds()

      data.forEach(place => {
        displayMarker(place)
        bounds.extend(new kakao.maps.LatLng(place.y, place.x))
      })

      map.value.setBounds(bounds)
      
      if (data.length === 1) {
        map.value.setLevel(2)
      } else {
        const currentLevel = map.value.getLevel()
        if (currentLevel > 7) {
          map.value.setLevel(7)
        }
      }
    }
  })
}

const displayMarker = (place) => {
  const marker = new kakao.maps.Marker({
    map: map.value,
    position: new kakao.maps.LatLng(place.y, place.x)
  })

  markers.value.push(marker)

  const infowindow = new kakao.maps.InfoWindow({
    content: `
      <div class="info-window">
        <div class="info-title">${place.place_name}</div>
        <div class="info-body">
          <div class="info-address">${place.address_name}</div>
          ${place.phone ? `
            <div class="info-phone">
              <span class="label">연락처:</span> ${place.phone}
            </div>
          ` : ''}
          ${place.road_address_name ? `
            <div class="info-road-address">
              <span class="label">도로명:</span> ${place.road_address_name}
            </div>
          ` : ''}
          <button class="find-route-btn" onclick="window.findRoute('${place.y}', '${place.x}', '${place.place_name}')">
            길찾기
          </button>
        </div>
      </div>
    `,
    removable: true
  })

  kakao.maps.event.addListener(marker, 'click', () => {
    closeActiveInfoWindow()
    infowindow.open(map.value, marker)
    activeInfoWindow.value = infowindow
  })

  kakao.maps.event.addListener(map.value, 'click', () => {
    closeActiveInfoWindow()
  })
}

// 길찾기 함수를 전역으로 등록
window.findRoute = (targetLat, targetLng, placeName) => {
  try {
    // 기존 경로선이 있다면 제거
    if (window.polylines) {
      window.polylines.forEach(line => line.setMap(null))
    }
    window.polylines = []

    // 기존 정보창이 있다면 제거
    const existingInfo = document.querySelector('.route-info')
    if (existingInfo) {
      existingInfo.remove()
    }

    // 출발지 좌표 (역삼동 718-5 기준)
    const startLat = 37.50110
    const startLng = 127.03674

    // 길찾기 URL 생성
    const routeUrl = `https://map.kakao.com/link/to/${placeName},${targetLat},${targetLng}/from/역삼동 718-5,${startLat},${startLng}`

    // 새 창에서 길찾기 페이지 열기
    window.open(routeUrl, '_blank')

    // 출발지와 도착지를 연결하는 선 그리기
    const linePath = [
      new kakao.maps.LatLng(startLat, startLng),
      new kakao.maps.LatLng(parseFloat(targetLat), parseFloat(targetLng))
    ]

    const polyline = new kakao.maps.Polyline({
      path: linePath,
      strokeWeight: 3,
      strokeColor: '#3B82F6',
      strokeOpacity: 0.7,
      strokeStyle: 'dashed'
    })

    polyline.setMap(map.value)
    window.polylines.push(polyline)

    // 경로가 모두 보이도록 지도 범위 조정
    const bounds = new kakao.maps.LatLngBounds()
    linePath.forEach(point => bounds.extend(point))
    map.value.setBounds(bounds)

    // 안내 메시지 표시
    const infoDiv = document.createElement('div')
    infoDiv.className = 'route-info'
    infoDiv.innerHTML = `
      <div class="route-info-content">
        <div class="route-summary">
          <div class="route-guide">※ 상세 경로는 새 창에서 확인하실 수 있습니다.</div>
          <div class="route-start">출발: 역삼동 718-5</div>
          <div class="route-end">도착: ${placeName}</div>
        </div>
      </div>
    `
    map.value.getNode().appendChild(infoDiv)

  } catch (error) {
    console.error('길찾기 오류:', error)
    alert('길찾기 기능 실행 중 오류가 발생했습니다.')
  }
}

onMounted(() => {
  if (!KAKAO_MAP_API_KEY) {
    console.error('카카오맵 API 키가 설정되지 않았습니다.')
    return
  }
  
  setTimeout(() => {
    initMap()
  }, 100)
})

onUnmounted(() => {
  closeActiveInfoWindow()
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
  map.value = null
  isScriptLoaded = false
})
</script>

<style scoped>
.map-wrapper {
  width: 100%;
  height: 100%;
  min-height: 400px;
  position: relative;
}

.map-container {
  width: 100%;
  min-height: 400px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  position: relative;
  z-index: 1;
  overflow: hidden;
}

/* Global styles for kakao map info window */
:global(.info-window) {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  min-width: 250px;
  max-width: 300px;
}

:global(.info-title) {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

:global(.info-body) {
  font-size: 0.875rem;
  color: #4a5568;
  line-height: 1.5;
}

:global(.info-address),
:global(.info-phone),
:global(.info-road-address) {
  margin-bottom: 0.5rem;
  word-break: keep-all;
  white-space: normal;
}

:global(.label) {
  font-weight: 500;
  color: #2d3748;
  margin-right: 0.25rem;
}

:global(.find-route-btn) {
  margin-top: 0.75rem;
  padding: 0.5rem 1rem;
  background-color: #3B82F6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.2s;
}

:global(.find-route-btn:hover) {
  background-color: #2563EB;
}

:global(.route-info) {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

:global(.route-summary) {
  font-size: 0.875rem;
  color: #4a5568;
}

:global(.route-guide) {
  color: #718096;
  font-size: 0.8rem;
  margin-bottom: 0.75rem;
}

:global(.route-start),
:global(.route-end) {
  color: #2d3748;
  margin-bottom: 0.25rem;
  font-weight: 500;
}
</style> 