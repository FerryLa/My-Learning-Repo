package com.ocean.testcrwaler.controller;

import com.ocean.testcrwaler.entity.News;
import com.ocean.testcrwaler.service.NewsService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/news")
@RequiredArgsConstructor
public class NewsController {
    private final NewsService newsService;

    @PostMapping
    public ResponseEntity<News> create(@RequestBody News news) {
        return ResponseEntity.ok(newsService.save(news));
    }

    @GetMapping
    public List<News> getAll() {
        return newsService.findAll();
    }

    @PutMapping("/{id}")
    public ResponseEntity<News> update(@RequestBody News news, @PathVariable Long id) {
        return ResponseEntity.ok(newsService.update(id, news));
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        newsService.delete(id);
    }
}
