# Используем современный и лёгкий Node.js
FROM node:20-alpine

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем package.json и package-lock.json (или yarn.lock)
# Если изменится package.json → npm install выполнится заново
COPY package*.json ./

# Устанавливаем зависимости (в том числе axios, react и т.д.)
RUN npm install

# Копируем весь проект в контейнер
COPY . .

# Открываем порт для Vite (по умолчанию 5173)
EXPOSE 5173

# Указываем хост 0.0.0.0, чтобы был доступен из контейнера
CMD ["npm", "run", "dev", "--", "--host"]
