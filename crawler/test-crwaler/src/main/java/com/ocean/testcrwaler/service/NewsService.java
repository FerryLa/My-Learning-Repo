package com.ocean.testcrwaler.service;

import com.ocean.testcrwaler.entity.News;
import com.ocean.testcrwaler.repository.NewsRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class NewsService {
    private final NewsRepository newsRepository;

    public News save(News news) {
        if (newsRepository.existsByUrl(news.getUrl())) { // 중복 제거
            throw new IllegalArgumentException("이미 존재하는 뉴스입니다.");
        }
        return newsRepository.save(news);
    }

    public List<News> findAll() {
        return newsRepository.findAll();
    }

    public News update(Long id, News updatedNews) {
        News news = newsRepository.findById(id).orElse(null);
        news.setTitle(updatedNews.getTitle());
        news.setContent(updatedNews.getContent());
        return newsRepository.save(news);
    }

    public void delete(Long id) {
        newsRepository.deleteById(id);
    }
}
