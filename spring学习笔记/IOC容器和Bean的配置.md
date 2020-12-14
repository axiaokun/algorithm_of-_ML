# IOC容器和Bean的配置

## IOC(Inversion of Control)：反转控制

IOC反转控制是一种设计思想，理解关键在于：控制

传统的方式是我们主动创建依赖对象，这样我们需要知道这些特定对象的获取方式，增加了学习成本，同时降低了开发效率。而IoC是有专门一个容器来创建这些对象，即由Ioc容器来控制对象的创建。

反转在于：

* 原来：我们主动去控制直接获取依赖对象
* 现在：容器帮我们查找注入依赖对象，不需要主动创建，只需要接受容器提供的依赖对象就行

## DI(Dependency Injection)：依赖注入

IOC的另一种表述方式：即组件以一些预先定义好的方式(例如：setter 方法)接受来自于容器的资源注入。相对于IOC而言，这种表述更直接。

总结: IOC 就是一种反转控制的思想， 而DI是对IOC的一种具体实现。

关于IOC和DI的概念可以参考[link](https://www.cnblogs.com/xdp-gacl/p/4249939.html#!comments)

## 获取bean

1. 通过id值从ioc容器中获取bean，id为配置spring管理的对象的唯一标示。
2. 从IOC容器中获取bean时，除了通过id值获取，还可以通过bean的类型获取。但如果同一个类型的bean在XML文件中配置了多个，则获取时会抛出异常，所以同一个类型的bean在容器中必须是唯一的。
3. 同时指定bean的id值和类型获取bean

## 依赖注入的方式

### 通过bean的setXxx()方法赋值

实际上原理是调用配置对象的对应属性的set方法，例子：

![](image\setXXX.png)

### 通过bean的构造器赋值

1. Spring自动匹配合适的构造器

   ```xml
   <bean id="s2" class="com.atguigu.spring.di.Student">
       <constructor-arg value="10086"></constructor-arg>
       <constructor-arg value="李四"></constructor-arg>
       <constructor-arg value="24"></constructor-arg>
       <constructor-arg value="女"></constructor-arg>
   </bean>
   ```

   

2. 通过索引值指定参数位置

   ```xml
   <bean id="s3" class="com.atguigu.spring.di.Student">
       <constructor-arg value="10022"></constructor-arg>
       <constructor-arg value="王五"></constructor-arg>
       <constructor-arg value="90" index="2"></constructor-arg>
       <constructor-arg value="女"></constructor-arg>
   </bean>
   ```

   

3. 通过类型区分重载的构造器

   ```xml
   <bean id="s3" class="com.atguigu.spring.di.Student">
       <constructor-arg value="10022"></constructor-arg>
       <constructor-arg value="王五"></constructor-arg>
       <constructor-arg value="90" type="java.lang.Double"></constructor-arg>
       <constructor-arg value="女"></constructor-arg>
   </bean>
   ```

   

### 通过注解的方式

使用注解一般是要使用自动装配。

关于自动装配：

自动装配：根据指定的装配规则，不需要明确指定，Spring自动将匹配的属性值注入bean中

* 装配规则
  * 根据类型自动装配：将类型匹配的bean作为属性注入到另一个bean中。若IOC容器中有多个与目标bean类型一致的bean，Spring将无法判定哪个bean最合适该属性，所以不能执行自动装配
  * 根据名称自动装配：必须将目标bean的名称和属性名设置的完全相同

也就是说，注解是自动装配的一种方式。

## 注解的类型

1.  普通组件：@Component  标识一个受Spring IOC容器管理的组件

2. 持久化层组件：@Repository  标识一个受Spring IOC容器管理的持久化层组件

3. 业务逻辑层组件：@Service  标识一个受Spring IOC容器管理的业务逻辑层组件

4. 表述层控制器组件：@Controller  标识一个受Spring IOC容器管理的表述层控制器组件

5. 组件的命名规则（id）

   1. 默认情况：使用组件的简单类名首字母小写后得到的字符串作为bean的id

   2. 使用组件注解的value属性指定bean的id

      指定id的方法，只需要在注解中的value值设置id

## 扫描组件

组件被上述注解标识后还需要通过Spring进行扫描才能够侦测到。

方法：

* 在xml配置文件中加入语句：

  ```xml
  <context:component-scan base-package="com.atguigu.component"/>
  ```

  相关属性说明：

  * base-package属性指定一个需要扫描的基类包，spring容器将会扫描这个基类包以及其子包中的所有类。

  * 当需要扫描多个包时可以使用逗号分隔

  * 如果仅希望扫描特定的类而非基包下的所有类，可使用resource-pattern属性过滤特定的类，示例：

    ```xml
    <context:component-scan 
    	base-package="com.atguigu.component" 
    	resource-pattern="autowire/*.class"/>
    ```

  * 包含与排除

    \<context:include-filter>子节点表示要包含的目标类，注意：通常需要与use-default-filters属性配合使用才能够达到“仅包含某些组件”这样的效果。即：通过将use-default-filters属性设置为false，禁用默认过滤器，然后扫描的就只是include-filter中的规则指定的组件了。

    \<context:exclude-filter>子节点表示要排除在外的目标类，同理此时use-default-filters属性需要设置为true。

    component-scan下可以拥有若干个include-filter和exclude-filter子节点

* 必须在原有JAR包组合的基础上再导入一个：spring-aop-4.0.0.RELEASE.jar

## 组件装配

* 需求

  ​	Controller组件中往往需要用到Service组件的实例，Service组件中往往需要用到	Repository组件的实例。Spring可以通过注解的方式帮我们实现属性的装配。

* 实现依据

  在指定要扫描的包时，\<context:component-scan> 元素会自动注册一个bean的后置处	理器：AutowiredAnnotationBeanPostProcessor的实例。该后置处理器可以自动装配标记	了**@Autowired**、@Resource或@Inject注解的属性

* @Autowired注解

  * 默认根据类型实现自动装配
  * 构造器、普通字段(即使是非public)、一切具有参数的方法都可以应用@Autowired注解
  * 默认情况下，所有使用@Autowired注解的属性都需要被设置。当Spring找不到匹配的bean装配属性时，会抛出异常。
  * 当byType实现不了装配时，会自动切换到byName，此时要求spring容器中，有一个bean的id和属性名一致
  * 若自动装配时，匹配到多个能够复制的bean，可使用@Qualifier(value="beanId")指定使用的bean，@Autowired和@Qualifier(value="beanId")可以一起作用域一个带形参的方法上，此时，@Qualifier(value="beanId")所指定的bean作用于形参，注意这里的beanId为指定的bean的类名，且首字母改为小写